hostname ${node.hostname}
password ${node.password}
% if node.ospf.logfile:
log file ${node.ospf.logfile}
% endif
% for section in node.ospf.debug:
debug ospf section
% endfor
!
% for intf in node.ospf.interfaces:
  interface ${intf.name}
  # ${intf.description}
  # Highiest priority routers will be DR
  ip ospf priority ${intf.ospf.priority}
  ip ospf cost ${intf.ospf.cost}
  # dead/hello intervals must be consistent across a broadcast domain
  ip ospf dead-interval ${intf.ospf.dead_int}
  ip ospf hello-interval ${intf.ospf.hello_int}
!
% endfor
router ospf
  router-id ${node.ospf.router_id}
  % if node.ospf.redistribute.fibbing:
  redistribute fibbing metric-type 1
  % endif
  % if node.ospf.redistribute.connected:
  redistribute connected metric-type 1 metric ${node.ospf.redistribute.connected}
  % endif
  % if node.ospf.redistribute.static:
  redistribute static metric-type 1 metric ${node.ospf.redistribute.static}
  % endif
  % for net in node.ospf.networks:
  network ${net.domain} area ${net.area}
  % endfor
!
