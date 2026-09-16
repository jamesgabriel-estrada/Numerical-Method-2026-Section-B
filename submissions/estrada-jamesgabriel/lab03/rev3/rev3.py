# solver_core.py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from unit_manager import UnitManager
from material_library import MaterialLibrary
from section_library import SectionLibrary

class StructuralModelRev2_3D:
    def __init__(self, unit_system="Metric"):
        self.units = UnitManager(system=unit_system)
        
        # Initialize libraries
        self.mat_lib = MaterialLibrary(default_grade="A36 Gr.36")
        self.steel_a36 = self.mat_lib.get_material()
        self.sec_lib = SectionLibrary()
        
        # Detailed profile mappings for each group
        self.members_config = {
            "Columns": {
                "profile": "W250X49.1", 
                "section": self.sec_lib.get_section("W10X49"), 
                "material_name": "A36 Gr.36",
                "material": self.steel_a36
            },
            "Roof Beams": {
                "profile": "W310X38.7", 
                "section": self.sec_lib.get_section("W12X26"), 
                "material_name": "A36 Gr.36",
                "material": self.steel_a36
            },
            "Tie Beams": {
                "profile": "W310X38.7", 
                "section": self.sec_lib.get_section("W8X31"), 
                "material_name": "A36 Gr.36",
                "material": self.steel_a36
            }
        }

    def generate_cube_geometry(self):
        # 6m x 6m cube coordinates (X, Y, Z)
        self.nodes = {
            1: [0.0, 0.0, 0.0],
            2: [6.0, 0.0, 0.0],
            3: [6.0, 6.0, 0.0],
            4: [0.0, 6.0, 0.0],
            5: [0.0, 0.0, 6.0],
            6: [6.0, 0.0, 6.0],
            7: [6.0, 6.0, 6.0],
            8: [0.0, 6.0, 6.0]
        }
        
        self.elements = [
            # Tie Beams (Bottom frame at Z = 0 -> mapped to XY plane)
            {"id": 1, "nodes": (1, 2), "type": "Tie Beams"},
            {"id": 2, "nodes": (2, 3), "type": "Tie Beams"},
            {"id": 3, "nodes": (3, 4), "type": "Tie Beams"},
            {"id": 4, "nodes": (4, 1), "type": "Tie Beams"},
            # Columns (Vertical members)
            {"id": 5, "nodes": (1, 5), "type": "Columns"},
            {"id": 6, "nodes": (2, 6), "type": "Columns"},
            {"id": 7, "nodes": (3, 7), "type": "Columns"},
            {"id": 8, "nodes": (4, 8), "type": "Columns"},
            # Roof Beams (Top frame at Z = 6)
            {"id": 9, "nodes": (5, 6), "type": "Roof Beams"},
            {"id": 10, "nodes": (6, 7), "type": "Roof Beams"},
            {"id": 11, "nodes": (7, 8), "type": "Roof Beams"},
            {"id": 12, "nodes": (8, 5), "type": "Roof Beams"}
        ]

    def plot_detailed_structural_model(self):
        self.generate_cube_geometry()
        
        fig = plt.figure(figsize=(11, 9))
        ax = fig.add_subplot(111, projection='3d')
        
        colors = {
            "Tie Beams": "#1f77b4", 
            "Columns": "#2ca02c", 
            "Roof Beams": "#ff7f0e"
        }
        
        # Plot elements and annotate each member at its midpoint with Profile + Material
        for el in self.elements:
            m_type = el["type"]
            config = self.members_config[m_type]
            
            n1, n2 = el["nodes"]
            p1 = np.array(self.nodes[n1])
            p2 = np.array(self.nodes[n2])
            
            # Draw member line
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 
                    color=colors[m_type], linewidth=3.5, label=m_type if el['id'] in [1,5,9] else "")
            
            # Calculate midpoint for text label placement
            midpoint = (p1 + p2) / 2.0
            label_text = f"{config['profile']} - {config['material_name']}"
            
            # Add text annotation on the 3D plot
            ax.text(midpoint[0], midpoint[1], midpoint[2], f"  {label_text}", 
                    fontsize=8, fontweight='bold', color='navy')

        # Plot nodes
        for node_id, coords in self.nodes.items():
            ax.scatter(coords[0], coords[1], coords[2], color='black', s=50)
            ax.text(coords[0], coords[1], coords[2], f" N{node_id}", fontsize=9)

        ax.set_xlabel("X (m) - lateral", fontweight='bold')
        ax.set_ylabel("Y (m) - lateral", fontweight='bold')
        ax.set_zlabel("Z (m) - vertical", fontweight='bold')
        ax.set_title("Structural model - cube_nodes_6m_rev2.xlsx", fontsize=13, fontweight='bold', pad=15)
        
        ax.legend(loc="upper left", frameon=True)
        print("[SUCCESS] Detailed 3D structural plot rendered with member profile and material tags!")
        plt.show()

if __name__ == "__main__":
    model = StructuralModelRev2_3D(unit_system="Metric")
    model.plot_detailed_structural_model()