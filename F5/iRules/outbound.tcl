when RULE_INIT {
    set static::outboundv4_debug 0
}
when CLIENT_ACCEPTED {
    if { [IP::addr [IP::local_addr] equals 211.146.16.254] }{
        pool pool_cw
    }
    elseif { [IP::addr [IP::local_addr] equals 223.70.139.94] }{
        pool pool_cmcc
    }
    elseif { [class match [IP::local_addr] equals public-dns] }{
        pool pool_cw
    }
    elseif { [class match [IP::local_addr] equals class_cmcc] }{
        pool pool_cmcc
    }
    else {
        pool pool_cw
    }
    if { $static::outboundv4_debug } { log local0. "#Client_Accept: IP.client_addr:[IP::client_addr] -> IP.local_addr:[IP::local_addr]" }
}
when LB_SELECTED {
    if { [IP::addr [LB::server addr] equals 211.146.16.254] }{
        snat automap
    }
    elseif { [IP::addr [LB::server addr] equals 223.70.139.94] }{
        snat automap
    }
    elseif { [class match [LB::server addr] equals public-dns] }{
        snat automap
    }
    elseif { [class match [LB::server addr] equals class_cmcc] }{
        snat automap
    }
    else {
        snat automap
    }
    if { $static::outboundv4_debug }{
        if { [LB::snat] eq "none" }{ log local0. "#LB_Selected: Snat disabled on [virtual name]" } 
        else { log local0. "#LB_Selected: Snat enabled on [virtual name]. Currently set to [LB::snat]"}
        # ClientSide

    }
}
when SERVER_CONNECTED {
    if { $static::outboundv4_debug }{
        set snat_ip [IP::local_addr]
        log local0. "#SNAT: $snat_ip"
        log local0. "#Server_Connected: IP.client_addr:[IP::client_addr] ; IP.local_addr:[IP::local_addr] -> IP.server_addr:[IP::server_addr]"
        # ServerSide
    }
}
