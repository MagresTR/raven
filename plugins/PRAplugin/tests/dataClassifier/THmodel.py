# Copyright 2017 Battelle Energy Alliance, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np

def run(self,Input):

  self.ACC_status = Input['ACC_status']
  self.time_LPI   = Input['time_LPI']
  self.time_LPR   = Input['time_LPR']

  timeToCD = 20.
  self.out = 0.

  if self.ACC_status == 1.:
    self.out = 1.

  self.LPI_act = self.time_LPI + 1 
  if self.time_LPI > timeToCD:
    self.out = 1.

<Input>ACC_status,time_LPI,time_LPR</Input>
<Output>out,ACC_act,LPI_act,LPR_act</Output>