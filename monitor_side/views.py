# from django.shortcuts import render
#
# # Create your views here.
# def pp(request):
#     ip = request.POST['adr_ip']
#
#     context = {'nom_periph': "nom",
#                'desc_pereph': "desc",
#                'nom_page': "monitoring",
#                'nom_periph': "snmp_walk(ip, comm, '1.3.6.1.2.1.1.5')",
#                'used_memory': "snmp_walk(ip, comm, '1.3.6.1.2.1.1.3')",
#                'free_ram': "snmp_walk(ip, comm, '1.3.6.1.4.1.9.9.48.1.1.1.5')",
#                }
#
#     return render(request, 'monitoring.html', context)

#python snmp trap receiver
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv

def receive_traps(request):
    snmpEngine = engine.SnmpEngine()

    TrapAgentAddress = '192.168.126.6';  # Trap listerner address
    Port = 162;  # trap listerner port

    print("Agent is listening SNMP Trap on " + TrapAgentAddress + " , Port : " + str(Port));
    print('--------------------------------------------------------------------------');
    config.addTransport(
        snmpEngine,
        udp.domainName + (1,),
        udp.UdpTransport().openServerMode((TrapAgentAddress, Port))
    )

    # Configure community here
    config.addV1System(snmpEngine, 'my-area', 'public')

    def cbFun(snmpEngine, stateReference, contextEngineId, contextName,
              varBinds, cbCtx):
        print("Received new Trap message");
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

    ntfrcv.NotificationReceiver(snmpEngine, cbFun)

    snmpEngine.transportDispatcher.jobStarted(1)

    try:
        snmpEngine.transportDispatcher.runDispatcher()
    except:
        snmpEngine.transportDispatcher.closeDispatcher()
        raise