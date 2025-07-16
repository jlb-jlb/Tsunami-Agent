rm -rf tsunami-agent-plugins/*
python3 cli.py -l
# python3 cli.py -v basket_access_and_manipulation

python3 cli.py -v xss
python3 cli.py -v unvalidated_redirects
python3 cli.py -v weak_password
python3 cli.py -v sql_injection
python3 cli.py -v directory_traversal
python3 cli.py -v vulnerable_components
python3 cli.py -v sensitive_data_exposure
python3 cli.py -v file_upload
python3 cli.py -v broken_access_control
python3 cli.py -v server_side_request_forgery
python3 cli.py -v xml_external_entity_xxe_injection
python3 cli.py -v broken_authentication
python3 cli.py -v insecure_deserialization
python3 cli.py -v improper_input_validation
