class OptionFacade(object):
    """Facade Class to price an option"""

    def __init__(self, option, engine, asset):
        self.option = option
        self.engine = engine
        self.asset = asset

    def price(self):
        return self.engine.pricing(self.option, self.asset)
