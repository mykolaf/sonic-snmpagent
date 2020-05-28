import os
import sys

# noinspection PyUnresolvedReferences
import tests.mock_tables.dbconnector

modules_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(modules_path, 'src'))

from unittest import TestCase

from ax_interface import ValueType
from ax_interface.pdu_implementations import GetPDU, GetNextPDU
from ax_interface.encodings import ObjectIdentifier
from ax_interface.constants import PduTypes
from ax_interface.pdu import PDU, PDUHeader
from ax_interface.mib import MIBTable
from sonic_ax_impl.mibs.ietf import rfc1213

class TestGetNextPDU(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lut = MIBTable(rfc1213.InterfacesMIB)
        for updater in cls.lut.updater_instances:
            updater.update_data()
            updater.reinit_data()
            updater.update_data()

    def test_getnextpdu_noneifindex(self):
        # oid.include = 1
        oid = ObjectIdentifier(10, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 1))
        get_pdu = GetNextPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        n = len(response.values)
        # self.assertEqual(n, 7)
        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.INTEGER)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 1, 1))))
        self.assertEqual(value0.data, 0)

    def test_getnextpdu_firstifindex(self):
        # oid.include = 1
        oid = ObjectIdentifier(9, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1))
        get_pdu = GetNextPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        n = len(response.values)
        # self.assertEqual(n, 7)
        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.INTEGER)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 1, 1))))
        self.assertEqual(value0.data, 0)

    def test_getnextpdu_secondifindex(self):
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 1, 1))
        get_pdu = GetNextPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        n = len(response.values)
        # self.assertEqual(n, 7)
        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.INTEGER)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 1, 5))))
        self.assertEqual(value0.data, 4)

    def test_regisiter_response(self):
        mib_2_response = b'\x01\x12\x10\x00\x00\x00\x001\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00,\x01d`\xab\x00\x00\x00\x00\x00\x05\x00\x00\x07\x04\x00\x00\x00\x00\x00\x01\x00\x00\x17\x8b\x00\x00\x00\x03\x00\x00\x00\n\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\t\x01\x12\x10\x00\x00\x00\x001\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x01d`\xab\x00\x00\x00\x00\x00\x05\x00\x00\x02\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02'
        # TODO: needs recursive response
        resp_pdu = PDU.decode(mib_2_response)
        print(resp_pdu)

    def test_interfaces_walk(self):
        resp = b'\x01\x06\x10\x00\x00\x00\x00C\x00\x01ay\x00\x01az\x00\x00\x00(\x06\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00}\x02\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x03'
        resp_pdu = PDU.decode(resp)
        resp_pdu.make_response(self.lut)
        print(resp_pdu)

    def test_oid_response(self):
        get_next = b'\x01\x06\x10\x00\x00\x00\x00I\x00\x01m\xe3\x00\x01m\xe4\x00\x00\x00(\x06\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x15\x00\x00\x00}\x02\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x03'

        pdu = PDU.decode(get_next)
        resp = pdu.make_response(self.lut)
        print(resp)

    def test_first_index(self):
        # walk
        walk = b'\x01\x06\x10\x00\x00\x00\x00O\x00\x01\x93\x9b\x00\x01\x93\x9c\x00\x00\x00(\x06\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x02\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x03'
        pdu = PDU.decode(walk)
        resp = pdu.make_response(self.lut)
        print(resp)

        # step
        step = b'\x01\x06\x10\x00\x00\x00\x00O\x00\x01\x94\x03\x00\x01\x94\x04\x00\x00\x00(\x06\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x05\x02\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x03'
        pdu = PDU.decode(step)
        resp = pdu.make_response(self.lut)
        print(resp)

    def test_bad_if_names(self):
        """
        Triggered by mis-configured interface names. Fine otherwise.
        TODO: exemplary bad DB
        """
        resp = b'\x01\x06\x10\x00\x00\x00\x00\x15\x00\x00\x01\x0c\x00\x00\x01\r\x00\x00\x00,\x06\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x1f\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x03\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x1f\x00\x00\x00\x02\x01\x06\x10\x00\x00\x00\x00\x15\x00\x00\x01\x12\x00\x00\x01\x13\x00\x00\x00,\x06\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x1f\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x03\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x1f\x00\x00\x00\x02\x01\x06\x10\x00\x00\x00\x00\x15\x00\x00\x01\x18\x00\x00\x01\x19\x00\x00\x00,\x06\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x1f\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x03\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x1f\x00\x00\x00\x02\x01\x06\x10\x00\x00\x00\x00\x15\x00\x00\x01\x1e\x00\x00\x01\x1f\x00\x00\x00,\x06\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x1f\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x03\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x1f\x00\x00\x00\x02'
        pdu = PDU.decode(resp)
        resp = pdu.make_response(self.lut)
        print(resp)

    def test_missing_counter(self):
        """
        KeyError: b'OUT_QLEN'
        counter_value = self.if_counters[sai_id][_table_name]
        snmp-subagent[242]: File "/usr/lib/python3.5/site-packages/ax_interface/mib.py", line 133, in __call__
        KeyError triggered when attribute is absent from interface counters.
        TODO: exemplary bad DB
        """
        resp = b'\x01\x06\x10\x00\x00\x00\x00[\x00\x00Ek\x00\x00En\x00\x00\x00(\x06\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x14\x00\x00\x00}\x02\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x03\x01\x06\x10\x00\x00\x00\x00[\x00\x00Eo\x00\x00Eq\x00\x00\x00(\x06\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x14\x00\x00\x00y\x02\x02\x00\x00\x00\x00\x00\x01\x00\x00\x00\x03'
        pdu = PDU.decode(resp)
        resp = pdu.make_response(self.lut)
        print(resp)

    def test_low_speed(self):
        """
        For an interface with a speed inside the 32 bit counter returns the speed of the interface in bps
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 5, 113))
        get_pdu = GetNextPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.GAUGE_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 5, 117))))
        self.assertEqual(value0.data, 1000000000)

    def test_high_speed(self):
        """
        For a speed higher than 4,294,967,295 the retrun should be 4294967295
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 5, 1))
        get_pdu = GetNextPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.GAUGE_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 5, 5))))
        self.assertEqual(value0.data, 4294967295)

    def test_no_speed(self):
        """
        For a port with no speed in the db the result should be 0
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 5, 117))
        get_pdu = GetNextPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.GAUGE_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 5, 121))))
        self.assertEqual(value0.data, 0)

    def test_if_type_eth(self):
        """
        For ethernet the type shpuld be 6
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 3, 1))
        get_pdu = GetNextPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.INTEGER)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 3, 5))))
        self.assertEqual(value0.data, 6)

    def test_if_type_portchannel(self):
        """
        For portchannel the type shpuld be 161
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 3, 1002))
        get_pdu = GetNextPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.INTEGER)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 3, 1003))))
        self.assertEqual(value0.data, 161)

    def test_mgmt_iface(self):
        """
        Test that mgmt port is present in the MIB
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 1, 10000))
        get_pdu = GetNextPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.INTEGER)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 1, 10001))))
        self.assertEqual(value0.data, 10000)

    def test_mgmt_iface_description(self):
        """
        Test mgmt port description (which is simply an alias)
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 2, 10001))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.OCTET_STRING)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 2, 10001))))
        self.assertEqual(str(value0.data), 'mgmt1')

    def test_mgmt_iface_oper_status(self):
        """
        Test mgmt port operative status
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 8, 10001))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.INTEGER)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 8, 10001))))
        self.assertEqual(value0.data, 1)

    def test_mgmt_iface_oper_status_unknown(self):
        """
        Test mgmt port operative status
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 8, 10002))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.INTEGER)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 8, 10002))))
        self.assertEqual(value0.data, 4)

    def test_mgmt_iface_admin_status(self):
        """
        Test mgmt port admin status
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 7, 10001))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.INTEGER)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 7, 10001))))
        self.assertEqual(value0.data, 1)

    def test_in_octets(self):
        """
        For a port with no speed in the db the result should be 0
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 10, 5))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.COUNTER_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 10, 5))))
        self.assertEqual(value0.data, 40321)

    def test_in_octets_override(self):
        """
        For a port with no speed in the db the result should be 0
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 10, 1))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.COUNTER_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 10, 1))))
        self.assertEqual(value0.data, 54321)

    def test_vlan_iface(self):
        """
        Test that vlan interface is present in the MIB
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 1, 2999))
        get_pdu = GetNextPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.INTEGER)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 1, 3000))))
        self.assertEqual(value0.data, 2999)

    def test_vlan_iface_description(self):
        """
        Test vlan interface description (which is simply the name)
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 2, 3000))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.OCTET_STRING)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 2, 3000))))
        self.assertEqual(str(value0.data), 'Vlan1000')

    def test_if_type_l3vlan(self):
        """
        For l3vlan the type shpuld be 136
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 3, 2000))
        get_pdu = GetNextPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.INTEGER)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 3, 3000))))
        self.assertEqual(value0.data, 136)

    def test_in_octets_rif(self):
        """
        For a port with RIF the counter values are aggregated
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 10, 21))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.COUNTER_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 10, 21))))
        self.assertEqual(value0.data, 2148)

    def test_in_ucast_rif(self):
        """
        For a port with RIF the counter values are aggregated
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 11, 21))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.COUNTER_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 11, 21))))
        self.assertEqual(value0.data, 110)

    def test_in_errors_rif(self):
        """
        For a port with RIF the counter values are aggregated
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 14, 21))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.COUNTER_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 14, 21))))
        self.assertEqual(value0.data, 101)

    def test_out_octets_rif(self):
        """
        For a port with RIF the counter values are aggregated
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 16, 21))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.COUNTER_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 16, 21))))
        self.assertEqual(value0.data, 4196)

    def test_out_ucast_rif(self):
        """
        For a port with RIF the counter values are aggregated
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 17, 21))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.COUNTER_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 17, 21))))
        self.assertEqual(value0.data, 120)

    def test_out_errors_rif(self):
        """
        For a port with RIF the counter values are aggregated
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 20, 21))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.COUNTER_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 20, 21))))
        self.assertEqual(value0.data, 102)

    def test_in_octets_vlan(self):
        """
        For a l3 Vlan values are mapped from RIF stats
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 10, 3000))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.COUNTER_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 10, 3000))))
        self.assertEqual(value0.data, 2048)

    def test_in_ucast_vlan(self):
        """
        For a l3 Vlan values are mapped from RIF stats
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 11, 3000))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.COUNTER_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 11, 3000))))
        self.assertEqual(value0.data, 10)

    def test_in_errors_vlan(self):
        """
        For a l3 Vlan values are mapped from RIF stats
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 14, 3000))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.COUNTER_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 14, 3000))))
        self.assertEqual(value0.data, 1)

    def test_out_octets_vlan(self):
        """
        For a l3 Vlan values are mapped from RIF stats
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 16, 3000))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.COUNTER_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 16, 3000))))
        self.assertEqual(value0.data, 4096)

    def test_out_ucast_vlan(self):
        """
        For a l3 Vlan values are mapped from RIF stats
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 17, 3000))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.COUNTER_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 17, 3000))))
        self.assertEqual(value0.data, 20)

    def test_out_errors_vlan(self):
        """
        For a l3 Vlan values are mapped from RIF stats
        """
        oid = ObjectIdentifier(11, 0, 0, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 20, 3000))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.COUNTER_32)
        self.assertEqual(str(value0.name), str(ObjectIdentifier(11, 0, 1, 0, (1, 3, 6, 1, 2, 1, 2, 2, 1, 20, 3000))))
        self.assertEqual(value0.data, 2)