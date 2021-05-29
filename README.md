**INSTALLING**

`git clone https://github.com/S3K-studio/sesc_backend.git`  
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