from alembic.operations import Operations, MigrateOperation
# http://alembic.zzzcomputing.com/en/latest/cookbook.html#replaceable-objects


class ReplaceableObject(object):
    def __init__(self, name, sqltext):
        self.name = name
        self.sqltext = sqltext


class ReversibleOp(MigrateOperation):
    def __init__(self, target):
        self.target = target

    @classmethod
    def invoke_for_target(cls, operations, target):
        op = cls(target)
        return operations.invoke(op)

    def reverse(self):
        raise NotImplementedError()

    @classmethod
    def _get_object_from_version(cls, operations, ident):
        version, objname = ident.split(".")

        module = operations.get_context().script.get_revision(version).module
        obj = getattr(module, objname)
        return obj

    @classmethod
    def replace(cls, operations, target, replaces=None, replace_with=None):

        if replaces:
            old_obj = cls._get_object_from_version(operations, replaces)
            drop_old = cls(old_obj).reverse()
            create_new = cls(target)
        elif replace_with:
            old_obj = cls._get_object_from_version(operations, replace_with)
            drop_old = cls(target).reverse()
            create_new = cls(old_obj)
        else:
            raise TypeError("replaces or replace_with is required")

        operations.invoke(drop_old)
        operations.invoke(create_new)


@Operations.register_operation("create_trigger", "invoke_for_target")
class CreateTriggerOp(ReversibleOp):
    def reverse(self):
        return DropTriggerOp(self.target)


@Operations.register_operation("drop_trigger", "invoke_for_target")
class DropTriggerOp(ReversibleOp):
    def reverse(self):
        return CreateTriggerOp(self.view)


@Operations.implementation_for(CreateTriggerOp)
def create_trigger(operations, operation):
    operations.execute("CREATE TRIGGER %s %s" % (
        operation.target.name,
        operation.target.sqltext
    ))


@Operations.implementation_for(DropTriggerOp)
def drop_trigger(operations, operation):
    operations.execute("DROP TRIGGER %s" % operation.target.name)
