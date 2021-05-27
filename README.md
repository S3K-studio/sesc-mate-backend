**INSTALLING**

`git clone https://github.com/S3K-studio/SESC_MATE-backend.git`  
`cd SESC_MATE-backend`  
`python3 -m venv venv`  
`pip install -r requirements.txt`  

**STARTING**

`python3 manage.py makemigrations`  
`python3 manage.py migrate`  
`python3 manage.py runserver`

*On Windows:*   
`celery -A sesc_mate worker --pool=solo`    
`celery -A sesc_mate beat`  

*On Linux:*   
`celery -A sesc_mate worker -B`