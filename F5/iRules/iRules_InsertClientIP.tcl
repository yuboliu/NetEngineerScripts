ltm rule /Common/insert_client_ip {
	when HTTP_REQUEST priority 100 {
	   HTTP::header insert infosec "[IP::client_addr]"
	}
}