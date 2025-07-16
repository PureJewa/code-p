import pyudev

# Voeg hier je Vendor/Product combinaties toe
DEVICES_TO_FIND = {
    "barcode_scanner": {"vendor": "0483", "product": "0011"},
    "arduino":         {"vendor": "2a03", "product": "003d"},  # Pas aan op jouw Arduino-model
}

def find_usb_device(name, vendor_id, product_id):
    context = pyudev.Context()
    for device in context.list_devices(subsystem='usb'):
        if device.get('ID_VENDOR_ID') == vendor_id and device.get('ID_MODEL_ID') == product_id:
            # Zoek naar corresponderend device node (ttyUSB*, ttyACM*, hidraw*, etc)
            for child in device.children:
                if child.device_node:
                    return {
                        "name": name,
                        "vendor": vendor_id,
                        "product": product_id,
                        "device_node": child.device_node,
                        "driver": child.driver,
                        "sys_name": child.sys_name
                    }
    return None

if __name__ == "__main__":
    for name, ids in DEVICES_TO_FIND.items():
        result = find_usb_device(name, ids['vendor'], ids['product'])
        if result:
            print(f"✅ {name} gevonden:")
            print(f"  ➤ Device node: {result['device_node']}")
            print(f"  ➤ Driver     : {result['driver']}")
            print(f"  ➤ Sys name   : {result['sys_name']}\n")
        else:
            print(f"❌ {name} niet gevonden.\n")
