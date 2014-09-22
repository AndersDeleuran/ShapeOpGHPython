///////////////////////////////////////////////////////////////////////////////
// This file is part of ShapeOp, a lightweight C++ library
// for static and dynamic geometry processing.
//
// Copyright (C) 2014 Sofien Bouaziz <sofien.bouaziz@gmail.com>
// Copyright (C) 2014 LGG EPFL
//
// This Source Code Form is subject to the terms of the Mozilla
// Public License v. 2.0. If a copy of the MPL was not distributed
// with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
///////////////////////////////////////////////////////////////////////////////
#ifndef API_H
#define API_H
///////////////////////////////////////////////////////////////////////////////
#include "Common.h"
///////////////////////////////////////////////////////////////////////////////
/** \file
* This file implements a C API for the ShapeOp C++ library.
*
* To use the library you need to:
*
* 1) Create the solver with #shapeop_create
*
* 2) Set the vertices with #shapeop_setPoints
*
* 3) Setup the constraints and forces
*
* 4) Initalize the solver with #shapeop_init or #shapeop_initDynamic
*
* 5) Optimize with #shapeop_solve
*
* 6) Get back the vertices with #shapeop_getPoints
*
* 7) Delete the solver with #shapeop_delete
*/
///////////////////////////////////////////////////////////////////////////////
/** \brief C structure that containts the C++ ShapeOp solver.*/
typedef struct ShapeOpSolver ShapeOpSolver;
///////////////////////////////////////////////////////////////////////////////
#ifdef __cplusplus
extern "C" {
#endif
///////////////////////////////////////////////////////////////////////////////
// Solver
/** \brief Create the ShapeOp solver. For more details see #ShapeOp::Solver.*/
SHAPEOP_API ShapeOpSolver *shapeop_create();
/** \brief Delete the ShapeOp solver. For more details see #ShapeOp::Solver.*/
SHAPEOP_API void shapeop_delete(ShapeOpSolver *op);
/** \brief Initialize the ShapeOp solver for static geometry processing. For more details see #ShapeOp::Solver.*/
SHAPEOP_API int  shapeop_init(ShapeOpSolver *op);
/** \brief Initialize the ShapeOp solver for dynamic geometry processing. For more details see #ShapeOp::Solver.*/
SHAPEOP_API int  shapeop_initDynamic(ShapeOpSolver *op,  ShapeOpScalar masses, ShapeOpScalar damping, ShapeOpScalar timestep);
/** \brief Run the optimization. For more details see #ShapeOp::Solver.*/
SHAPEOP_API int  shapeop_solve(ShapeOpSolver *op, unsigned int iteration);

/** \brief Set the vertices to the ShapeOp solver. For more details see #ShapeOp::Solver.*/
SHAPEOP_API void shapeop_setPoints(ShapeOpSolver *op, ShapeOpScalar *points, int nb_points);
/** \brief Get the vertices back from the ShapeOp solver. For more details see #ShapeOp::Solver.*/
SHAPEOP_API void shapeop_getPoints(ShapeOpSolver *op, ShapeOpScalar *points, int nb_points);

/** \brief Set the timestep of the ShapeOp solver. For more details see #ShapeOp::Solver.*/
SHAPEOP_API void shapeop_setTimeStep(ShapeOpSolver *op, ShapeOpScalar timestep);
/** \brief Set the damping of the ShapeOp solver. For more details see #ShapeOp::Solver.*/
SHAPEOP_API void shapeop_setDamping(ShapeOpSolver *op, ShapeOpScalar damping);

/** \brief Run the optimization. For more details see #ShapeOp::Solver.*/
SHAPEOP_API ShapeOpScalar shapeop_getConstraintError(ShapeOpSolver *op, int constraint_id);
///////////////////////////////////////////////////////////////////////////////
// Constraints
/** \brief Add an edge strain constraint to the ShapeOp solver. For more details see #ShapeOp::EdgeStrainConstraint.*/
SHAPEOP_API int shapeop_addEdgeStrainConstraint(ShapeOpSolver *op, int id1, int id2, ShapeOpScalar weight);
/** \brief Edit an edge strain constraint previously added to the ShapeOp solver. For more details see #ShapeOp::EdgeStrainConstraint.*/
SHAPEOP_API void shapeop_editEdgeStrainConstraint(ShapeOpSolver *op, int constraint_id, ShapeOpScalar length);

/** \brief Add a triangle strain constraint to the ShapeOp solver. For more details see #ShapeOp::TriangleStrainConstraint.*/
SHAPEOP_API int shapeop_addTriangleStrainConstraint(ShapeOpSolver *op, int id1, int id2, int id3, ShapeOpScalar weight);

/** \brief Add a tetrahedron strain constraint to the ShapeOp solver. For more details see #ShapeOp::TetrahedronStrainConstraint.*/
SHAPEOP_API int shapeop_addTetrahedronStrainConstraint(ShapeOpSolver *op, int id1, int id2, int id3, int id4, ShapeOpScalar weight);

/** \brief Add an area constraint to the ShapeOp solver. For more details see #ShapeOp::AreaConstraint.*/
SHAPEOP_API int shapeop_addAreaConstraint(ShapeOpSolver *op, int id1, int id2, int id3, ShapeOpScalar weight);

/** \brief Add a volume constraint to the ShapeOp solver. For more details see #ShapeOp::VolumeConstraint.*/
SHAPEOP_API int shapeop_addVolumeConstraint(ShapeOpSolver *op, int id1, int id2, int id3, int id4, ShapeOpScalar weight);

/** \brief Add a bending constraint to the ShapeOp solver. For more details see #ShapeOp::BendingConstraint.*/
SHAPEOP_API int shapeop_addBendingConstraint(ShapeOpSolver *op, int *ids, int nb_ids, ShapeOpScalar weight);

/** \brief Add a closeness constraint to the ShapeOp solver. For more details see #ShapeOp::ClosenessConstraint.*/
SHAPEOP_API int shapeop_addClosenessConstraint(ShapeOpSolver *op, int id, ShapeOpScalar weight);
/** \brief Edit a closeness constraint previously added to the ShapeOp solver. For more details see #ShapeOp::ClosenessConstraint.*/
SHAPEOP_API void shapeop_editClosenessConstraint(ShapeOpSolver *op, int constraint_id, ShapeOpScalar *point);

/** \brief Add a line constraint to the ShapeOp solver. For more details see #ShapeOp::LineConstraint.*/
SHAPEOP_API int shapeop_addLineConstraint(ShapeOpSolver *op, int *ids, int nb_ids, ShapeOpScalar weight);

/** \brief Add a plane constraint to the ShapeOp solver. For more details see #ShapeOp::PlaneConstraint.*/
SHAPEOP_API int shapeop_addPlaneConstraint(ShapeOpSolver *op, int *ids, int nb_ids, ShapeOpScalar weight);

/** \brief Add a circle constraint to the ShapeOp solver. For more details see #ShapeOp::CircleConstraint.*/
SHAPEOP_API int shapeop_addCircleConstraint(ShapeOpSolver *op, int *ids, int nb_ids, ShapeOpScalar weight);

/** \brief Add a sphere constraint to the ShapeOp solver. For more details see #ShapeOp::SphereConstraint.*/
SHAPEOP_API int shapeop_addSphereConstraint(ShapeOpSolver *op, int *ids, int nb_ids, ShapeOpScalar weight);

/** \brief Add a uniform laplacian constraint to the ShapeOp solver. For more details see #ShapeOp::UniformLaplacianConstraint.*/
SHAPEOP_API int shapeop_addUniformLaplacianConstraint(ShapeOpSolver *op, int *ids, int nb_ids, int displacement_lap, ShapeOpScalar weight);
///////////////////////////////////////////////////////////////////////////////
// Forces
/** \brief Add a gravity force to the ShapeOp solver. For more details see #ShapeOp::GravityForce.*/
SHAPEOP_API int shapeop_addGravityForce(ShapeOpSolver *op, ShapeOpScalar *force);

/** \brief Add a vertex force to the ShapeOp solver. For more details see #ShapeOp::VertexForce.*/
SHAPEOP_API int shapeop_addVertexForce(ShapeOpSolver *op, ShapeOpScalar *force, int id);
/** \brief Edit a vertex force previously added to the ShapeOp solver. For more details see #ShapeOp::VertexForce.*/
SHAPEOP_API void shapeop_editVertexForce(ShapeOpSolver *op, int force_id, ShapeOpScalar *force, int id);
///////////////////////////////////////////////////////////////////////////////
#ifdef __cplusplus
}
#endif
///////////////////////////////////////////////////////////////////////////////
#endif // API_H
///////////////////////////////////////////////////////////////////////////////