source env/bin/activate

python3 scraper.py

sleep 15

python3 features.py

sleep 15

python3 reconcile.py

sleep 15

python3 tweet.py

deactivate

git add mdb.csv

git commit -m "weekly update"

git push origin master
