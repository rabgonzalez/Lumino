from factory import Faker, RelatedFactoryList


class UniqueFaker(Faker):
    """A Faker that always returns unique values.
    https://github.com/FactoryBoy/factory_boy/pull/820#issuecomment-1004802669"""

    @classmethod
    def _get_faker(cls, locale=None):
        return super()._get_faker(locale=locale).unique


class RelatedFactoryVariableList(RelatedFactoryList):
    """Allows overriding ``size`` during factory usage, e.g. ParentFactory(list_factory__size=4)
    https://github.com/FactoryBoy/factory_boy/issues/767#issuecomment-1139185137"""

    def call(self, instance, step, context):
        size = context.extra.pop('size', self.size)
        assert isinstance(size, int)
        return [super(RelatedFactoryList, self).call(instance, step, context) for i in range(size)]
