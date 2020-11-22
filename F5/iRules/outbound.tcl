ltm rule /Common/insert_client_ip {
    when CLIENT_ACCEPTED priority 100 {
        if { [IP::addr [IP::local_addr] equals 211.156.138.57] }{
            pool pool_cw
        }
        elseif { [IP::addr [IP::local_addr] equals 36.110.104.241] }{
            pool pool_cmcc
        }
        elseif { class match [IP::local_addr] equals class_cw }{
            pool pool_cw
        }
        elseif { class match [IP::local_addr] equals class_cmcc }{
            pool pool_cmcc
        }
        else {
            pool default_gateway
        }

    }
    when LB_SELECTED priority 200 {
        if { [IP::addr [IP::server addr] equals 211.156.138.57] }{
            snat automap
        }
        elseif { [IP::addr [IP::server addr] equals 36.110.104.241] }{
            snat automap
        }
        elseif { class match [IP::server addr] equals class_cw }{
            snat automap
        }
        elseif { class match [IP::server addr] equals class_cmcc }{
            snat automap
        }
        else {
            snat automap
        }
    }
}