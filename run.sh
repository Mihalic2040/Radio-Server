#screen -dmS update ./run_parser.sh
./run_parser.sh

#uwsgi --socket 0.0.0.0:5000 --protocol=http -w app:app -p 10 --enable-threads
