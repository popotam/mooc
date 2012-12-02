// Transform.cpp: implementation of the Transform class.

// Note: when you construct a matrix using mat4() or mat3(), it will be COLUMN-MAJOR
// Keep this in mind in readfile.cpp and display.cpp
// See FAQ for more details or if you're having problems.

#include <cmath>
#include <cstdio>
#include "Transform.h"

// Helper rotation function.  Please implement this.  
mat3 Transform::rotate(const float degrees, const vec3& a)
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

void Transform::left(float degrees, vec3& eye, vec3& up) 
{
  printf("eye: %.2f, %.2f, %.2f; dist: %.2f; up: %.2f, %.2f\n", eye.x, eye.y,
      eye.z, sqrt(pow(eye.x, 2) + pow(eye.y, 2) + pow(eye.z, 2)), up.x, up.y,
      up.z);
  eye = eye * rotate(degrees, up);
}

void Transform::up(float degrees, vec3& eye, vec3& up) 
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

mat4 Transform::lookAt(const vec3 &eye, const vec3 &center, const vec3 &up) 
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

mat4 Transform::perspective(float fovy, float aspect, float zNear, float zFar)
{
  float top = zNear * tan(fovy * M_PI / 360.0);
  float right = top * aspect;
  mat4 dest = frustum(-right, right, -top, top, zNear, zFar);
  return dest;
}

mat4 Transform::frustum(
		const float left, const float right,
		const float bottom, const float top,
		const float near, const float far) {
    float rl = (right - left);
    float tb = (top - bottom);
    float fn = (far - near);
    mat4 dest = mat4(
    		(near * 2) / rl, 0, (right + left) / rl, 0,
    		0, (near * 2) / tb, (top + bottom) / tb, 0,
    		0, 0, -(far + near) / fn,  -(far * near * 2) / fn,
    		0, 0, -1, 0);
    return dest;
}

mat4 Transform::scale(const float &sx, const float &sy, const float &sz) 
{
    return mat4(
        sx, 0, 0, 0,
        0, sy, 0, 0,
        0, 0, sz, 0,
        0, 0, 0, 1);
}

mat4 Transform::translate(const float &tx, const float &ty, const float &tz) 
{
    return mat4(
        1, 0, 0, tx,
        0, 1, 0, ty,
        0, 0, 1, tz,
        0, 0, 0, 1);
}

// To normalize the up direction and construct a coordinate frame.  
// As discussed in the lecture.  May be relevant to create a properly 
// orthogonal and normalized up. 
// This function is provided as a helper, in case you want to use it. 
// Using this function (in readfile.cpp or display.cpp) is optional.  

vec3 Transform::upvector(const vec3 &up, const vec3 & zvec) 
{
    vec3 x = glm::cross(up,zvec); 
    vec3 y = glm::cross(zvec,x); 
    vec3 ret = glm::normalize(y); 
    return ret; 
}


Transform::Transform()
{

}

Transform::~Transform()
{

}
