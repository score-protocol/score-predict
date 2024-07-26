# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
# Copyright © 2023 <your name>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


import time
import os
import wandb
# Bittensor
import bittensor as bt

# Bittensor Validator Template:
import scorepredict
from scorepredict.validator import forward
from scorepredict import __version__

# import base validator class which takes care of most of the boilerplate
from scorepredict.base.validator import BaseValidatorNeuron
from scorepredict.utils.utils import set_simulated_time, get_current_time
from datetime import datetime, time as dt_time


class Validator(BaseValidatorNeuron):
    """
    Your validator neuron class. You should use this class to define your validator's behavior. In particular, you should replace the forward function with your own logic.

    This class inherits from the BaseValidatorNeuron class, which in turn inherits from BaseNeuron. The BaseNeuron class takes care of routine tasks such as setting up wallet, subtensor, metagraph, logging directory, parsing config, etc. You can override any of the methods in BaseNeuron if you need to customize the behavior.

    This class provides reasonable default behavior for a validator such as keeping a moving average of the scores of the miners and using them to set weights at the end of each epoch. Additionally, the scores are reset for new hotkeys at the end of each epoch.
    """

    def __init__(self, config=None):
        super(Validator, self).__init__(config=config)

        bt.logging.info("load_state()")
        self.load_state()

                # Set up simulated time if enabled
        if self.config.simulate_time:
            # Set initial simulated time to 2 PM UTC of the current day
            initial_time = datetime.utcnow().replace(hour=14, minute=0, second=0, microsecond=0)
            set_simulated_time(initial_time)
            bt.logging.debug(f"Simulated time initialized to: {get_current_time(self)}")
        else:
            bt.logging.debug(f"Using real time: {datetime.now(time.utc)}")

        # TODO(developer): Anything specific to your use case you can do here
        
        #netrc_path = pathlib.Path.home() / ".netrc"
        #wandb_api_key = os.getenv("WANDB_API_KEY")
        #if wandb_api_key is not None:
        #    bt.logging.info("WANDB_API_KEY is set")
        #bt.logging.info("~/.netrc exists:", netrc_path.exists())

        #if wandb_api_key is None :
        #    bt.logging.warning(
        #        "WANDB_API_KEY not found in environment variables."
        #    )
        
        # wandb.init(
        #         project=f"sn{self.config.netuid}-validators",
        #         entity="score",
        #         config={
        #             "hotkey": self.wallet.hotkey.ss58_address,
        #         },
        #         name=f"validator-{self.uid}-{__version__}",
        #         resume="auto",
        #         dir=self.config.neuron.full_path,
        #         reinit=True,
        # )

    async def forward(self):
        """
        Validator forward pass. Consists of:
        - Generating the query
        - Querying the miners
        - Getting the responses
        - Rewarding the miners
        - Updating the scores
        """
        # TODO(developer): Rewrite this function based on your protocol definition.
        return await forward(self)


# The main function parses the configuration and runs the validator.
if __name__ == "__main__":
    with Validator() as validator:
        while True:
            bt.logging.info(f"Validator running... {time.time()}")
            time.sleep(5)
