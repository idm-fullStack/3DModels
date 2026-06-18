import numpy as np
import trimesh
import os

def generate_perfect_closed_globox():
    if os.path.exists('globox_avatar.gltf'):
        os.remove('globox_avatar.gltf')
        

    BLUE = (30, 120, 200, 255)
    YELLOW = (195, 235, 140, 255)
    WHITE = (255, 255, 255, 255)
    BLACK = (10, 10, 10, 255)
    RED_MOUTH = (140, 15, 25, 255)

   
    scene = trimesh.Scene()

    # 1. КОРПУС
    body_base = trimesh.creation.icosphere(subdivisions=3, radius=0.85)
    body_base.apply_transform(np.diag([1.2, 1.2, 1.0, 1.0]))
    body_base.apply_translation([0, -0.2, -0.05])
    body_base.visual.face_colors = BLUE
    scene.add_geometry(body_base, node_name="Body")
    
    body_neck = trimesh.creation.icosphere(subdivisions=3, radius=0.6)
    body_neck.apply_transform(np.diag([1.0, 0.9, 0.8, 1.0]))
    body_neck.apply_translation([0, 0.35, -0.1])
    body_neck.visual.face_colors = BLUE
    scene.add_geometry(body_neck, node_name="Neck")

    belly = trimesh.creation.icosphere(subdivisions=3, radius=0.75)
    belly.apply_transform(np.diag([1.15, 1.15, 0.5, 1.0]))
    belly.apply_translation([0, -0.15, 0.55])
    belly.visual.face_colors = YELLOW
    scene.add_geometry(belly, node_name="Belly")

    # 2. МОРДА
    mouth_base = trimesh.creation.icosphere(subdivisions=3, radius=0.9)
    mouth_base.apply_transform(np.diag([1.25, 0.40, 1.0, 1.0]))
    mouth_base.apply_translation([0, 0.70, 0.05])
    mouth_base.visual.face_colors = BLUE
    scene.add_geometry(mouth_base, node_name="MouthBase")

    # ГЛАЗА
    eye_l_geo = trimesh.creation.icosphere(subdivisions=3, radius=0.20)
    eye_l_geo.apply_transform(np.diag([0.85, 1.2, 0.85, 1.0]))
    eye_l_geo.apply_translation([-0.09, 1.0, 0.15])
    eye_l_geo.visual.face_colors = WHITE
    scene.add_geometry(eye_l_geo, node_name="EyeL")
    
    pupil_l = trimesh.creation.icosphere(subdivisions=2, radius=0.045)
    pupil_l.apply_translation([-0.05, 1.16, 0.31])
    pupil_l.visual.face_colors = BLACK
    scene.add_geometry(pupil_l, node_name="PupilL")

    eye_r_geo = trimesh.creation.icosphere(subdivisions=3, radius=0.20)
    eye_r_geo.apply_transform(np.diag([0.85, 1.2, 0.85, 1.0]))
    eye_r_geo.apply_translation([0.09, 1.0, 0.15])
    eye_r_geo.visual.face_colors = WHITE
    scene.add_geometry(eye_r_geo, node_name="EyeR")
    
    pupil_r = trimesh.creation.icosphere(subdivisions=2, radius=0.045)
    pupil_r.apply_translation([0.04, 1.16, 0.31])
    pupil_r.visual.face_colors = BLACK
    scene.add_geometry(pupil_r, node_name="PupilR")

 
    mouth_yellow = trimesh.creation.icosphere(subdivisions=3, radius=0.88)
    mouth_yellow.apply_transform(np.diag([1.23, 0.22, 1.05, 1.0]))
    mouth_yellow.apply_translation([0, 0.52, 0.10])
    mouth_yellow.visual.face_colors = YELLOW
    scene.add_geometry(mouth_yellow, node_name="Mouth")

    inner_mouth = trimesh.creation.icosphere(subdivisions=2, radius=0.4)
    inner_mouth.apply_transform(np.diag([1.4, 0.4, 0.4, 1.0]))
    inner_mouth.apply_translation([0, 0.60, -0.1])
    inner_mouth.visual.face_colors = RED_MOUTH
    scene.add_geometry(inner_mouth, node_name="InnerMouth")

    # 3. РУКИ С ЛОКТЯМИ 
    arm_radius = 0.065
    
    l_shoulder = [-0.85, 0.1, 0.3]
    l_elbow = [-1.0, -0.2, 0.5]      
    l_wrist = [-0.9, -0.6, 0.55]     
    
    r_shoulder = [0.85, 0.1, 0.3]
    r_elbow = [1.0, -0.2, 0.5]       
    r_wrist = [0.9, -0.6, 0.55]      
    
    # Левая рука
    scene.add_geometry(trimesh.creation.cylinder(radius=arm_radius, segment=[l_shoulder, l_elbow], sections=16), node_name="ArmL_Upper")
    scene.add_geometry(trimesh.creation.cylinder(radius=arm_radius * 0.92, segment=[l_elbow, l_wrist], sections=16), node_name="ArmL_Lower")
    
    elbow_joint_l = trimesh.creation.icosphere(subdivisions=2, radius=arm_radius * 1.1)
    elbow_joint_l.apply_translation(l_elbow)
    elbow_joint_l.visual.face_colors = BLUE
    scene.add_geometry(elbow_joint_l, node_name="ArmL_Elbow")
    
    # Правая рука
    scene.add_geometry(trimesh.creation.cylinder(radius=arm_radius, segment=[r_shoulder, r_elbow], sections=16), node_name="ArmR_Upper")
    scene.add_geometry(trimesh.creation.cylinder(radius=arm_radius * 0.92, segment=[r_elbow, r_wrist], sections=16), node_name="ArmR_Lower")
    
    elbow_joint_r = trimesh.creation.icosphere(subdivisions=2, radius=arm_radius * 1.1)
    elbow_joint_r.apply_translation(r_elbow)
    elbow_joint_r.visual.face_colors = BLUE
    scene.add_geometry(elbow_joint_r, node_name="ArmR_Elbow")

    # 4. КИСТИ 
    def create_hand_mesh(pos_x, pos_y, pos_z, is_left=True):
        hand_parts = []
        
        palm = trimesh.creation.box(extents=[0.3, 0.35, 0.14])
        palm.apply_transform(trimesh.transformations.rotation_matrix(np.radians(80), [1, 0, 0]))
        palm.apply_translation([pos_x, pos_y - 0.05, pos_z + 0.08])
        palm.visual.face_colors = YELLOW
        hand_parts.append(palm)
        
        finger_positions = [
            (-0.1, -0.06, 0.25),
            (-0.03, -0.06, 0.27),
            (0.04, -0.06, 0.27),
            (0.11, -0.06, 0.25)
        ]
        
        if not is_left:
            finger_positions = [(-x, y, z) for x, y, z in finger_positions]
        
        for fx, fy, fz in finger_positions:
            finger = trimesh.creation.box(extents=[0.08, 0.08, 0.18])
            finger.apply_transform(trimesh.transformations.rotation_matrix(np.radians(80), [1, 0, 0]))
            finger.apply_translation([pos_x + fx, pos_y + fy - 0.03, pos_z + fz])
            finger.visual.face_colors = YELLOW
            hand_parts.append(finger)
        
        thumb = trimesh.creation.box(extents=[0.12, 0.1, 0.11])
        thumb_offset_x = -0.2 if is_left else 0.2
        thumb.apply_transform(trimesh.transformations.rotation_matrix(np.radians(80), [1, 0, 0]))
        thumb.apply_transform(trimesh.transformations.rotation_matrix(np.radians(20), [0, 1, 0]))
        thumb.apply_translation([pos_x + thumb_offset_x, pos_y - 0.03, pos_z + 0.13])
        thumb.visual.face_colors = YELLOW
        hand_parts.append(thumb)
            
        
        return trimesh.util.concatenate(hand_parts)
    
    left_hand = create_hand_mesh(l_wrist[0], l_wrist[1], l_wrist[2], is_left=True)
    scene.add_geometry(left_hand, node_name="HandL")
    
    right_hand = create_hand_mesh(r_wrist[0], r_wrist[1], r_wrist[2], is_left=False)
    scene.add_geometry(right_hand, node_name="HandR")

    # 5. НОГИ
    scene.add_geometry(trimesh.creation.cylinder(radius=0.13, height=0.35, sections=16).apply_translation([-0.5, -0.85, 0.2]), node_name="LegL")
    scene.add_geometry(trimesh.creation.cylinder(radius=0.13, height=0.35, sections=16).apply_translation([0.5, -0.85, 0.2]), node_name="LegR")

    # 6. СТУПНИ
    def create_plush_foot(pos_x, is_left=True):
        foot_parts = []
        base_yaw = np.radians(25) if is_left else np.radians(-25)
        for i in range(3):
            toe = trimesh.creation.icosphere(subdivisions=3, radius=0.22)
            toe.apply_transform(np.diag([0.85, 0.45, 2.0, 1.0]))
            toe_angle = np.radians((i - 1) * 28)
            toe.apply_transform(trimesh.transformations.rotation_matrix(toe_angle + base_yaw, [0, 1, 0]))
            x_offset = (i - 1) * 0.28
            z_offset = 0.25 - abs(i - 1) * 0.06
            toe.apply_translation([pos_x + x_offset, -1.0, 0.2 + z_offset])
            toe.visual.face_colors = YELLOW
            foot_parts.append(toe)
        return trimesh.util.concatenate(foot_parts)
    
    scene.add_geometry(create_plush_foot(-0.6, is_left=True), node_name="FootL")
    scene.add_geometry(create_plush_foot(0.6, is_left=False), node_name="FootR")



if __name__ == "__main__":
    generate_perfect_closed_globox()
