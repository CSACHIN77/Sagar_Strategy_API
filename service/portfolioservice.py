
from repo.portfoliorepo import PortfolioRepo
import json

        
class Portfolioservice:
    def __init__(self,data):
        self.data = data
        #self.strategyId = strategyId
    
    def process_insert_data(self, data,):
        strategy = Strategy(id = data['id'], name= data['name'])        #.straddle_repo.insert_strategy_data(self.id,self.name,self.underlying,self.strategy_type,self.implied_futures_expiry,self.entry_time,self.last_entry_time
                                                #,self.exit_time,self.square_off,self.overall_sl,self.overall_target,self.trailing_options,self.profit_reaches
                                                #,self.lock_profit,self.increase_in_profit,self.trail_profit)
        #print(strategy)
        
        legs = []
        #print(data['strategies'][0]['legs'])

        for strategy_data in data['strategies']:
        # Create a Leg object for each strategy
            leg = Leg(
                strategy_id=strategy_data['strategy_id'],
                symbol=strategy_data['symbol'],
                quantity_multiplier=strategy_data['quantity_multiplier'],
                monday=strategy_data['monday'],
                tuesday=strategy_data['tuesday'],
                wednesday=strategy_data['wednesday'],
                thrusday=strategy_data['thrusday'],
                friday=strategy_data['friday']
            # Add other attributes as per your Leg model
            )
        # Append the leg to the list of legs
            legs.append(leg)
            #print(leg.position)

        #print(len(legs))
            
        # Do data validation
        
        # Pass data to repo
        repo = PortfolioRepo()
        repo.insert_data(strategy,legs)
        
      
    def process_update_data(self, data,strategyId):
    
        strategy = Strategy(id = data['id'], name= data['name'])
        print(strategy)
            
        legs = []
            #print(data['strategies'][0]['legs'])

        for strategy_data in data['strategies']:
            # Create a Leg object for each strategy
            leg = Leg(
                strategy_id=strategy_data['strategy_id'],
                symbol=strategy_data['symbol'],
                quantity_multiplier=strategy_data['quantity_multiplier'],
                monday=strategy_data['monday'],
                tuesday=strategy_data['tuesday'],
                wednesday=strategy_data['wednesday'],
                thrusday=strategy_data['thrusday'],
                friday=strategy_data['friday']
                # Add other attributes as per your Leg model
            )
            # Append the leg to the list of legs
            legs.append(leg)
                #print(leg.position)

            #print(len(legs))
                
            # Do data validation
            
            # Pass data to repo
        repo = PortfolioRepo()
        repo.update_data(strategy,legs,strategyId)
    
    def getAllPortfolioDetails(self):
        repo = PortfolioRepo()
        strategy_name = repo.getAllPortfolio()
        return strategy_name
    
    def getPortfolioDetails(self, strategyId):
        print(strategyId)
        repo = PortfolioRepo()
        strategy_details = repo.getPortfolioDetails(strategyId)
        return strategy_details
    
class Strategy:
    def __init__(self,id:int,name:str):
        #print(id)
        self.id = id
        self.name=name
        
        #print(self.id)

    def _repr_(self):
        #print(self.id)
        return f"Strategy(id={self.id},name={self.name})"
    

class Leg:
    def __init__(self,strategy_id:int,symbol:str,quantity_multiplier:int,monday:bool,tuesday:bool,wednesday:bool,thrusday:bool,friday:bool):
            #print(id)
            #print(position)
        self.strategy_id = strategy_id
        self.symbol = symbol
        self.quantity_multiplier = quantity_multiplier
        self.monday = bool(monday)  # Convert to boolean
        self.tuesday = bool(tuesday)  # Convert to boolean
        self.wednesday = bool(wednesday)
        self.thrusday = bool(thrusday)
        self.friday = bool(friday)
            
    def _repr_(self):
        #print(self.id)
        return f"Leg(strategy_id={self.strategy_id},symbol={self.symbol},quantity_multiplier={self.quantity_multiplier},monday={self.monday},tuesday={self.tuesday},wednesday={self.wednesday},thrusday={self.thrusday},friday={self.friday})"