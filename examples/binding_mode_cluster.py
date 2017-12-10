from alphaspace import *
import mdtraj
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist, squareform
from scipy.cluster.hierarchy import fcluster, linkage, dendrogram
import os
from itertools import combinations_with_replacement

print(os.getcwd())

# here is a script to cluster binding mode in a trajectory or series of snapshots of same system.
# The binding mode are encoded in the contact atom Jaccard difference matrix, which can be the distance matrix
# used for clustering algorithm.


# load system
universe = AS_Universe()
for i in range(1, 1 + 10):
    test_ligand_path = 'alphaspace/tests/bcl2/lig/{}.pdb'.format(i)
    test_protein_path = 'alphaspace/tests/bcl2/prot/{}.pdb'.format(i)
    ligand = mdtraj.load(test_ligand_path)
    protein = mdtraj.load(test_protein_path)
    universe.set_receptor(protein, append=True)
    universe.set_binder(ligand, append=True)

universe.config.screen_by_face = True
universe.run_alphaspace()

face_atoms = universe._get_face_atoms()

contact_fingerprint_matrices = []

for snapshot_idx in universe.snapshots_indices:
    receptor_coords = universe.receptor.traj.xyz[snapshot_idx]
    binder_coords = universe.binder.traj.xyz[snapshot_idx]

    binder_to_receptor_dist = cdist(binder_coords, receptor_coords)

    contact_atoms = (binder_to_receptor_dist < 4.0) * face_atoms[snapshot_idx]

    contact_fingerprint_matrices.append(contact_atoms)

distance_matrix = np.zeros((len(contact_fingerprint_matrices), len(contact_fingerprint_matrices)))
for i, j in combinations_with_replacement(range(len(distance_matrix)), 2):
    if i == j:
        distance_matrix[i][j] = 0
        continue

    overlap = np.sum(contact_fingerprint_matrices[i] * contact_fingerprint_matrices[j], axis=1)
    union = np.sum((contact_fingerprint_matrices[i] + contact_fingerprint_matrices[j]) > 0, axis=1)
    distance = np.average(overlap / union)
    distance_matrix[i][j] = distance_matrix[j][i] = 1 - distance

pocket_d_idx = list(fcluster(Z=linkage(squareform(distance_matrix), method='average'),
                             t=0.75, criterion='distance') - 1)

plt.figure()
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(linkage(squareform(distance_matrix), method='average'),
           leaf_rotation=90,  # rotates the x axis labels
           leaf_font_size=8,  # font size for the x axis labels
           )
plt.show()