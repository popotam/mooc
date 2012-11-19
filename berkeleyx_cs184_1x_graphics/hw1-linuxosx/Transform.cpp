// Transform.cpp: implementation of the Transform class.

#include "stdio.h"
#include "Transform.h"

//Please implement the following functions:

// Helper rotation function.  
mat3
Transform::rotate(const float degrees, const vec3& a)
{
  float theta = degrees * pi/180.0;
  mat3 rotation = (
      cos(theta) * mat3(1, 0, 0,
                        0, 1, 0,
                        0, 0, 1) +
      (1 - cos(theta)) * mat3(a.x * a.x, a.x * a.y, a.x * a.z,
                              a.y * a.x, a.y * a.y, a.y * a.z,
                              a.z * a.x, a.z * a.y, a.z * a.z) +
      sin(theta) * mat3(0, -a.z, a.y,
                        a.z, 0, -a.x,
                        -a.y, a.x, 0)
  );
  return rotation;
}

// Transforms the camera left around the "crystal ball" interface
void
Transform::left(float degrees, vec3& eye, vec3& up)
{
  printf("eye: %.2f, %.2f, %.2f; dist: %.2f; up: %.2f, %.2f\n", eye.x, eye.y,
      eye.z, sqrt(pow(eye.x, 2) + pow(eye.y, 2) + pow(eye.z, 2)), up.x, up.y,
      up.z);
  eye = eye * rotate(degrees, up);
}

// Transforms the camera up around the "crystal ball" interface
void
Transform::up(float degrees, vec3& eye, vec3& up)
{
  printf("eye: %.2f, %.2f, %.2f; dist: %.2f; up: %.2f, %.2f\n", eye.x, eye.y,
      eye.z, sqrt(pow(eye.x, 2) + pow(eye.y, 2) + pow(eye.z, 2)), up.x, up.y,
      up.z);
  vec3 ortho_axis = glm::cross(eye, up);
  ortho_axis = glm::normalize(ortho_axis);
  mat3 rotation = rotate(degrees, ortho_axis);
  eye = eye * rotate(degrees, ortho_axis);
  up = up * rotate(degrees, ortho_axis);
}

// Your implementation of the glm::lookAt matrix
mat4
Transform::lookAt(vec3 eye, vec3 up)
{
  vec3 w = glm::normalize(eye);
  vec3 u = glm::normalize(glm::cross(up, w));
  vec3 v = glm::cross(w, u);
  mat4 look_at = mat4(
      u.x, u.y, u.z, -glm::dot(u, eye),
      v.x, v.y, v.z, -glm::dot(v, eye),
      w.x, w.y, w.z, -glm::dot(w, eye),
      0, 0, 0, 1);
  return look_at;
}

Transform::Transform()
{

}

Transform::~Transform()
{

}
