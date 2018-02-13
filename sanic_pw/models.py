import peewee as pw


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""
    # This requires a bit of explanation: the basic idea is to make a
    # dummy metaclass for one level of class instantiation that replaces
    # itself with the actual metaclass.
    class metaclass(type):
        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)
    return type.__new__(metaclass, 'temporary_class', (), {})


class Signal(object):
    """
    Simplest signals implementation for Peewee ORM.
    """
    __slots__ = 'receivers'

    def __init__(self):
        """
        Initialize the signal.
        """
        self.receivers = []

    def connect(self, receiver):
        """
        Append receiver.
        """
        if not callable(receiver):
            raise ValueError('Invalid receiver: %s' % receiver)
        self.receivers.append(receiver)

    def __call__(self, receiver):
        """
        Support decorators.
        """
        self.connect(receiver)
        return receiver

    def disconnect(self, receiver):
        """
        Remove receiver.
        """
        try:
            self.receivers.remove(receiver)
        except ValueError:
            raise ValueError('Unknown receiver: %s' % receiver)

    def send(self, instance, *args, **kwargs):
        """
        Send signal.
        """
        for receiver in self.receivers:
            receiver(instance, *args, **kwargs)


class BaseSignalModel(pw.BaseModel):
    """
    Special metaclass that provides an opportunity to use pre/post signals
    with instances of a model.
    """
    models = []

    def __new__(mcs, name, bases, attrs):
        cls = super(BaseSignalModel, mcs).__new__(mcs, name, bases, attrs)
        cls.pre_save = Signal()
        cls.pre_delete = Signal()
        cls.post_delete = Signal()
        cls.post_save = Signal()

        if cls._meta.db_table and cls._meta.db_table != 'model':
            mcs.models.append(cls)

        cls._meta.read_slaves = getattr(cls._meta, 'read_slaves', None)
        return cls


class Model(with_metaclass(BaseSignalModel, pw.Model)):

    @classmethod
    def select(cls, *args, **kwargs):
        """
        Support read slaves.
        """
        query = super(Model, cls).select(*args, **kwargs)
        query.database = cls._get_read_database()
        return query

    @classmethod
    def raw(cls, *args, **kwargs):
        """
        Send a raw SQL query to the database. If was specified
        the `select` operator, then the query will be sent to
        the a suitable slave node.
        """
        query = super(Model, cls).raw(*args, **kwargs)
        if query._sql.lower().startswith('select'):
            query.database = cls._get_read_database()
        return query

    @property
    def pk(self):
        """
        Return primary key value.
        """
        return self._get_pk_value()

    @classmethod
    def get_or_none(cls, *args, **kwargs):
        try:
            return cls.get(*args, **kwargs)
        except cls.DoesNotExist:
            return None

    def save(self, force_insert=False, **kwargs):
        """
        Invoke pre- and post-signals during saves.
        """
        created = force_insert or not bool(self.pk)
        self.pre_save.send(self, created=created)
        super(Model, self).save(force_insert=force_insert, **kwargs)
        self.post_save.send(self, created=created)

    def delete_instance(self, *args, **kwargs):
        """
        Invoke pre- and post-signals during deleting an object.
        """
        self.pre_delete.send(self)
        super(Model, self).delete_instance(*args, **kwargs)
        self.post_delete.send(self)

    @classmethod
    def _get_read_database(cls):
        if not cls._meta.read_slaves:
            return cls._meta.database
        current_idx = getattr(cls, '_read_slave_idx', -1)
        cls._read_slave_idx = (current_idx + 1) % len(cls._meta.read_slaves)
        return cls._meta.read_slaves[cls._read_slave_idx]
