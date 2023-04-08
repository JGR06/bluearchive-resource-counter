import os
import sys
import shutil
import xml.etree.ElementTree as elementTree


resolutions_root = './image_variants'
dst_xml = '../resource_counter/resource_counter.xml'
dest_images_root = '../resource_counter/image'


def replace_assets_xml(src_xml):
    # NOTE: element_tree.XMLParser(encoding='euc-kr') not worked
    with open(src_xml, 'r', encoding='euc-kr') as f:
        replace_to = elementTree.fromstring(f.read())
        f.close()

    with open(dst_xml, 'r', encoding='euc-kr') as f:
        target = elementTree.fromstring(f.read())
        f.close()
    asset_node = target.find('GENERAL')
    for child in asset_node:
        if 'Image_' not in child.tag:
            continue
        for node in child:
            if node.tag in ['Rect', 'ROI']:
                # element.find() has no attribute '__enter__' -- I can't use 'with' statement
                name = child.find('Name')
                to = None
                if name is not None:
                    found = replace_to.find(f".//*/[Name='{name.text}']")
                    to = found.find(node.tag)
                if to is not None:
                    print(f"{name.text}/{node.tag}: rewrite to {to.text} from {node.text}")
                    node.text = to.text
    root = elementTree.ElementTree(target)
    root.write(dst_xml, encoding='EUC-KR')  # original encoding text was capital word


def overwrite_images(src_dir):
    files = os.listdir(src_dir)
    for file in files:
        src_path = os.path.join(src_dir, file)
        dst_path = os.path.join(dest_images_root, file)
        shutil.copy2(src_path, dst_path)


if __name__ == '__main__':
    for arg in sys.argv:
        print(arg)

    if len(sys.argv) < 4:
        print('Insufficient params')
        raise Exception

    width = int(sys.argv[1])
    height = int(sys.argv[2])
    dpi = int(sys.argv[3])
    filename = f'{resolutions_root}/{width}_{height}_{dpi}dpi.xml'
    if os.path.isfile(filename):
        replace_assets_xml(filename)
    else:
        raise FileExistsError

    src_images_dir = f'{resolutions_root}/{width}_{height}_{dpi}dpi'
    overwrite_images(src_images_dir)
