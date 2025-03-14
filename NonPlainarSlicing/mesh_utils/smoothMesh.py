import trimesh
import numpy as np
import globals


def smoothMesh(mesh: trimesh.Trimesh, angle: float, tol=1e-6) -> trimesh.Trimesh:
    vertices = mesh.vertices.copy()
    faces = mesh.faces.copy()

    
    globals.progress2 = 0
    change = np.inf
    count = 0
    max_count = len(vertices)
    while change > tol:
        prev_vertices = vertices.copy()
        # Process all vertices (possibly in a fixed order or via BFS)
        globals.progress2 = count / float(max_count)
        

        for i in range(len(vertices)):

            
            # Here, you might use a fixed order rather than re-sorting every time.
            # Alternatively, you can structure your propagation differently.
            neighbors_faces = faces[np.any(faces == i, axis=1)]
            neighbors = np.unique(neighbors_faces.ravel())
            z_min_v = vertices[i]
            # Clamp neighbors above z_min + max_z_diff.
            vertices[neighbors, 2] = np.where(vertices[neighbors, 2] > z_min_v[2] + np.arctan(np.radians(angle)) * np.sqrt( np.square(vertices[neighbors, 0] - z_min_v[0]) + np.square(vertices[neighbors, 1] - z_min_v[1]) ), 
                                              z_min_v[2] + np.arctan(np.radians(angle)) * np.sqrt( np.square(vertices[neighbors, 0] - z_min_v[0]) + np.square(vertices[neighbors, 1] - z_min_v[1]) ),
                                              vertices[neighbors, 2])
        change = np.abs(vertices - prev_vertices).max()

        count_cnage = np.sum(vertices[:,2] == prev_vertices[:,2])
        count = count_cnage
        
        globals.progress2 = 0

    return trimesh.Trimesh(vertices=vertices, faces=faces)


