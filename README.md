**INSTALLING**

`git clone https://github.com/S3K-studio/sesc-mate-backend.git`  
`cd sesc_backend`  
`python3 -m venv venv`  
`pip install -r requirements.txt`  

**STARTING**

`python3 manage.py createcachetable`  
`python3 manage.py migrate`  
`python3 manage.py runserver`

*On Windows:*   
`celery -A sesc_mate worker --pool=solo`    
`celery -A sesc_mate beat`  

*On Linux:*   
`celery -A sesc_mate worker -B`

---

**SESC MATE: Backend** — VK MiniApp for easy viewing of the schedule and announcements of the SESC UrFU.

Copyright (C) 2019-2021  The Authors.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
