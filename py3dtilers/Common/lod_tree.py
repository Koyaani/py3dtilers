from ..Common import GeometryTree, GeometryNode, Lod1Node, LoaNode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Common import Groups


class LodTree(GeometryTree):
    """
    The LodTree contains the root node(s) of the LOD hierarchy and the centroid of the whole tileset
    """

    def __init__(self, groups: 'Groups', create_lod1=False, create_loa=False, with_texture=False, geometric_errors=[None, None, None]):
        """
        LodTree takes an instance of FeatureList (which contains a collection of Feature) and creates nodes.
        In order to reduce the number of .b3dm, it also distributes the features into a list of Group.
        A Group contains features and an optional polygon that will be used for LoaNodes.
        """
        root_nodes = list()

        for group in groups:
            node = GeometryNode(group.feature_list, geometric_errors[0], with_texture)
            root_node = node
            if create_lod1:
                lod1_node = Lod1Node(node, geometric_errors[1])
                lod1_node.add_child_node(root_node)
                root_node = lod1_node
            if create_loa:
                loa_node = LoaNode(node, geometric_errors[2], group.polygons)
                loa_node.add_child_node(root_node)
                root_node = loa_node

            root_nodes.append(root_node)

        super().__init__(root_nodes)
