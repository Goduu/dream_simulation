from langchain_test.main import main
from langchain_test.action_mask_agent import ActionMaskAgent
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
import slidezoo as sz

load_dotenv()

def tic_tac_toe():
    from pettingzoo.classic import tictactoe_v3

    env = tictactoe_v3.env(render_mode="human")
    agents = {
        name: ActionMaskAgent(name=name, model=ChatOpenAI(temperature=0.2), env=env)
        for name in env.possible_agents
    }
    main(agents, env)
    
tic_tac_toe()