import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class ProjectDatabaseLoader:
    """Safely loads data from Excel files with built-in fallbacks if files are not found."""
    def __init__(self):
        try:
            self.units_df = pd.read_excel('Units_Imperial_Metric.xlsx', sheet_name='Unit Systems', header=3)
        except Exception:
            self.units_df = None

        try:
            self.materials_df = pd.read_excel('RISA_Materials_Library.xlsx', sheet_name='All Materials', header=3)
        except Exception:
            self.materials_df = None

        try:
            self.aisc_df = pd.read_excel('aisc-shapes-database-v160-2.xlsx', sheet_name='Database v16.0', header=0)
        except Exception:
            self.aisc_df = None

    def get_material(self, label="A36 Gr.36", system="Metric"):
        if self.materials_df is not None:
            row = self.materials_df[self.materials_df['Label'].str.contains(label, case=False, na=False)]
            if not row.empty:
                r = row.iloc[0]
                if system == "Imperial":
                    return {
                        "Type": r['Category'], "Label": r['Label'],
                        "E": r['E [ksi]'], "G": r['G [ksi]'],
                        "Fy": r['Yield / f\'c / f\'m [ksi]'], "Fu": r['Fu [ksi]'],
                        "Density": r['Density [k/ft³]']
                    }
                else:
                    return {
                        "Type": r['Category'], "Label": r['Label'],
                        "E": r['E [MPa]'], "G": r['G [MPa]'],
                        "Fy": r['Yield / f\'c / f\'m [MPa]'], "Fu": r['Fu [MPa]'],
                        "Density": r['Mass Density [kg/m³]']
                    }
        if system == "Imperial":
            return {"Type": "Hot Rolled", "Label": "A36 Gr.36", "E": 29000.0, "G": 11154.0, "Fy": 36.0, "Fu": 58.0, "Density": 0.49}
        else:
            return {"Type": "Hot Rolled", "Label": "A36 Gr.36 (Hot Rolled)", "E": 199948.0, "G": 76904.0, "Fy": 248.2, "Fu": 399.9, "Density": 76.97}

    def get_section(self, shape_label):
        if self.aisc_df is not None:
            row = self.aisc_df[self.aisc_df['AISC_Manual_Label'] == shape_label]
            if not row.empty:
                r = row.iloc[0]
                return {"Label": r['AISC_Manual_Label'], "A": r['A'], "Ix": r['Ix'], "Iy": r['Iy'], "J": r['J']}
        fallbacks = {
            "W12X53": {"Label": "W12X53", "A": 15.6, "Ix": 425.0, "Iy": 57.7, "J": 2.15},
            "W12X26": {"Label": "W12X26", "A": 7.65, "Ix": 204.0, "Iy": 17.3, "J": 0.54}
        }
        return fallbacks.get(shape_label, {"Label": shape_label, "A": 10.0, "Ix": 150.0, "Iy": 50.0, "J": 1.0})

class StructuralSolver3D:
    """3D Structural Solver with complete Rev. 3 detailing and visualization."""
    def __init__(self, unit_system="Metric"):
        self.db = ProjectDatabaseLoader()
        self.system = unit_system.capitalize()
        
        if self.system == "Imperial":
            self.force_unit = "kip"
            self.length_unit = "ft"
            self.stress_unit = "ksi"
        else:
            self.force_unit = "kN"
            self.length_unit = "m"
            self.stress_unit = "MPa"

        self.nodes = pd.DataFrame(columns=['NodeID', 'X', 'Y', 'Z', 'Support', 'DOF_Start', 'DOF_End'])
        self.members = pd.DataFrame(columns=['MemberID', 'i', 'j', 'Type', 'Profile', 'Release_i', 'Release_j', 'BetaAngle'])

    def add_node(self, node_id, x, y, z, support='Free'):
        dof_start = (node_id - 1) * 6 + 1
        dof_end = node_id * 6
        new_row = pd.DataFrame([{
            'NodeID': node_id, 'X': float(x), 'Y': float(y), 'Z': float(z),
            'Support': support, 'DOF_Start': dof_start, 'DOF_End': dof_end
        }])
        self.nodes = pd.concat([self.nodes, new_row], ignore_index=True)

    def add_member(self, member_id, node_i, node_j, member_type, release_i='None', release_j='None', beta_angle=0.0):
        if member_type == "Column":
            profile = "W12X53"
        elif member_type in ["RoofBeam", "TieBeam"]:
            profile = "W12X26"
        else:
            raise ValueError("Invalid member type specified.")

        new_row = pd.DataFrame([{
            'MemberID': member_id, 'i': node_i, 'j': node_j,
            'Type': member_type, 'Profile': profile,
            'Release_i': release_i, 'Release_j': release_j, 'BetaAngle': beta_angle
        }])
        self.members = pd.concat([self.members, new_row], ignore_index=True)

    def render_model(self):
        fig = plt.figure(figsize=(16, 9))

        # Main Title & Subtitle with Section B
        fig.suptitle(
            '6m x 6m x 6m Cube - Structural Model, Rev. 3 (Numerical Methods - Sec B)\nPinned supports, global/local axes, beta angles, MZ end releases | Units: Metric', 
            fontsize=11, 
            fontweight='bold', 
            y=0.95
        )

        # 3D Model Subplot
        ax = fig.add_subplot(121, projection='3d')

        free_nodes = self.nodes[self.nodes['Support'] == 'Free']
        pinned_nodes = self.nodes[self.nodes['Support'] == 'Pinned']

        ax.scatter(
            free_nodes['X'].to_numpy(dtype=float), 
            free_nodes['Y'].to_numpy(dtype=float), 
            free_nodes['Z'].to_numpy(dtype=float), 
            color='salmon', s=50, label='Free node'
        )
        ax.scatter(
            pinned_nodes['X'].to_numpy(dtype=float), 
            pinned_nodes['Y'].to_numpy(dtype=float), 
            pinned_nodes['Z'].to_numpy(dtype=float), 
            color='red', s=80, label='Supported node (pinned)'
        )

        for _, node in self.nodes.iterrows():
            ax.text(node['X'], node['Y'] + 0.3, node['Z'], f"N{int(node['NodeID'])}\nDOF {int(node['DOF_Start'])}-{int(node['DOF_End'])}", fontsize=8, color='black', ha='center')
            if node['Support'] == 'Pinned':
                ax.plot([node['X']-0.3, node['X']+0.3, node['X']], [node['Y']-0.5, node['Y']-0.5, node['Y']], [node['Z'], node['Z'], node['Z']], color='gray', linewidth=2)

        for _, member in self.members.iterrows():
            node_i = self.nodes[self.nodes['NodeID'] == member['i']].iloc[0]
            node_j = self.nodes[self.nodes['NodeID'] == member['j']].iloc[0]
            
            is_column = member['Type'] == 'Column'
            line_color = 'forestgreen' if is_column else 'navy'
            ax.plot([node_i['X'], node_j['X']], [node_i['Y'], node_j['Y']], [node_i['Z'], node_j['Z']], color=line_color, linewidth=2)
            
            mid_x = (node_i['X'] + node_j['X']) / 2
            mid_y = (node_i['Y'] + node_j['Y']) / 2
            mid_z = (node_i['Z'] + node_j['Z']) / 2
            
            beta_str = f" (beta={int(member['BetaAngle'])} deg)" if member['BetaAngle'] != 0 else ""
            label_text = f"M{member['MemberID']}{beta_str}"
            if member['Release_i'] != 'None' or member['Release_j'] != 'None':
                label_text += " [MZ]"
                ax.scatter([node_i['X'], node_j['X']], [node_i['Y'], node_j['Y']], [node_i['Z'], node_j['Z']], facecolors='none', edgecolors='red', s=60, linewidths=1.5)

            ax.text(mid_x, mid_y, mid_z, f" {label_text}", fontsize=7, color='darkblue', fontweight='bold')

            if is_column:
                ax.quiver(mid_x, mid_y, mid_z, 0.6, 0, 0, color='red', linewidth=1.5, arrow_length_ratio=0.3)
                ax.quiver(mid_x, mid_y, mid_z, 0, 0.6, 0, color='green', linewidth=1.5, arrow_length_ratio=0.3)
                ax.quiver(mid_x, mid_y, mid_z, 0, 0, 0.6, color='purple', linewidth=1.5, arrow_length_ratio=0.3)

        # Global Origin & Coordinate Arrows
        ax.quiver(0, 0, 0, 1.5, 0, 0, color='darkorange', linewidth=2, arrow_length_ratio=0.2)
        ax.quiver(0, 0, 0, 0, 1.5, 0, color='blue', linewidth=2, arrow_length_ratio=0.2)
        ax.quiver(0, 0, 0, 0, 0, 1.5, color='saddlebrown', linewidth=2, arrow_length_ratio=0.2)
        ax.text(1.7, 0, 0, 'Global X', color='darkorange', fontweight='bold', fontsize=8)
        ax.text(0, 1.7, 0, 'Global Y', color='blue', fontweight='bold', fontsize=8)
        ax.text(0, 0, 1.7, 'Global Z', color='saddlebrown', fontweight='bold', fontsize=8)
        ax.scatter([0], [0], [0], color='green', marker='*', s=120, label='Origin (0, 0, 0)')

        ax.set_xlabel('X (m) - lateral', fontweight='bold')
        ax.set_ylabel('Y (m) - vertical', fontweight='bold')
        ax.set_zlabel('Z (m) - lateral', fontweight='bold')
        ax.set_xlim(-1, 7)
        ax.set_ylim(-1, 7)
        ax.set_zlim(-1, 7)

        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], color='navy', lw=2, label='Beam'),
            Line2D([0], [0], color='forestgreen', lw=2, label='Column'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Supported node (pinned)'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='salmon', markersize=8, label='Free node'),
            plt.Line2D([0], [0], marker='o', color='red', markerfacecolor='none', markersize=8, label='Pinned member end (MZ released)'),
            plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='green', markersize=10, label='Origin (0, 0, 0)'),
            Line2D([0], [0], color='red', lw=1.5, label='Local x axis'),
            Line2D([0], [0], color='green', lw=1.5, label='Local y axis'),
            Line2D([0], [0], color='purple', lw=1.5, label='Local z axis'),
            Line2D([0], [0], color='darkorange', lw=1.5, label='Global X axis'),
            Line2D([0], [0], color='blue', lw=1.5, label='Global Y axis'),
            Line2D([0], [0], color='saddlebrown', lw=1.5, label='Global Z axis'),
        ]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=7, framealpha=0.9)

        # Right-side Model Data Information Text Panel
        ax_text = fig.add_subplot(122)
        ax_text.axis('off')

        model_text = """MODEL DATA - REV. 3 (SEC B)
-------------------------------------------------------------
Analyst Details
  Analyst            James Gabriel Estrada
  Course / Section   Numerical Methods (Sec B)
  Instructor         Engr. Mark Airol Escranda

Units
  System             metric
  Internal set       kN, m
  Length             m
  Section dim        mm
  Stress             MPa
  Density            kN/m³

Geometry
  Cube edge          6.0 m
  Nodes              8
  Members            12

Supports
  Type               pinned
  Nodes              1, 2, 3, 4
  Restrained         UX, UY, UZ
  Released           RX, RY, RZ

Default material
  Label              A36 Gr.36 (Hot Rolled)
  E                  199948.0 MPa / 199.9 GPa
  Fy                 248.2 MPa
  Fu                 399.9 MPa
  nu                 0.30
  gamma              76.97 kN/m³
  alpha              11.7 e-6/degC

Sections
  Tie beam           W12X26 / W12X26
  Roof beam          W12X26 / W12X26
  Column             W12X53 / W12X53

Nodal DOF
  Per node           6
  Total              48
  Restrained         12
  Active             36

Member end releases
  Pinned members     M1, M3, M5, M7
  Pattern            Pinned i and j
  Component          MZ (moment about local z)
  Symbol             hollow circle at the end

Beta angles
  Base / roof beams  0 deg
  Columns            90 deg
"""

        ax_text.text(0.02, 0.98, model_text, fontsize=7.5, family='monospace', verticalalignment='top', 
                     bbox=dict(boxstyle='round', facecolor='aliceblue', edgecolor='steelblue', alpha=0.9))

        plt.subplots_adjust(top=0.88, bottom=0.05, left=0.04, right=0.96)
        plt.savefig('cube_structure_Rev3.png', dpi=300)
        plt.show()

# --- Execution ---
if __name__ == "__main__":
    solver = StructuralSolver3D(unit_system="Metric")

    # Define 8 Nodes for the 6m x 6m x 6m Cube Framework
    solver.add_node(1, 0.0, 0.0, 0.0, support='Pinned')
    solver.add_node(2, 6.0, 0.0, 0.0, support='Pinned')
    solver.add_node(3, 6.0, 0.0, 6.0, support='Pinned')
    solver.add_node(4, 0.0, 0.0, 6.0, support='Pinned')
    solver.add_node(5, 0.0, 6.0, 0.0, support='Free')
    solver.add_node(6, 6.0, 6.0, 0.0, support='Free')
    solver.add_node(7, 6.0, 6.0, 6.0, support='Free')
    solver.add_node(8, 0.0, 6.0, 6.0, support='Free')

    # Define 12 Members with releases on M1, M3, M5, M7 and beta angles on columns (90 deg)
    solver.add_member(1, 1, 2, "TieBeam", release_i='MZ', release_j='MZ', beta_angle=0.0)
    solver.add_member(2, 2, 3, "TieBeam", beta_angle=0.0)
    solver.add_member(3, 3, 4, "TieBeam", release_i='MZ', release_j='MZ', beta_angle=0.0)
    solver.add_member(4, 4, 1, "TieBeam", beta_angle=0.0)

    solver.add_member(5, 5, 6, "RoofBeam", release_i='MZ', release_j='MZ', beta_angle=0.0)
    solver.add_member(6, 6, 7, "RoofBeam", beta_angle=0.0)
    solver.add_member(7, 7, 8, "RoofBeam", release_i='MZ', release_j='MZ', beta_angle=0.0)
    solver.add_member(8, 8, 5, "RoofBeam", beta_angle=0.0)

    solver.add_member(9, 1, 5, "Column", beta_angle=90.0)
    solver.add_member(10, 2, 6, "Column", beta_angle=90.0)
    solver.add_member(11, 3, 7, "Column", beta_angle=90.0)
    solver.add_member(12, 4, 8, "Column", beta_angle=90.0)

    solver.render_model()