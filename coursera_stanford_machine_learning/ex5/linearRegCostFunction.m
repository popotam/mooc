function [J, grad] = linearRegCostFunction(X, y, theta, lambda)
%LINEARREGCOSTFUNCTION Compute cost and gradient for regularized linear 
%regression with multiple variables
%   [J, grad] = LINEARREGCOSTFUNCTION(X, y, theta, lambda) computes the 
%   cost of using theta as the parameter for linear regression to fit the 
%   data points in X and y. Returns the cost in J and the gradient in grad

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost and gradient of regularized linear 
%               regression for a particular choice of theta.
%
%               You should set J to the cost and grad to the gradient.
%

n = size(theta, 1);

hth = X * theta;

J = (1 / (2 * m)) * sum((hth - y) .^ 2) ...
	+ (lambda / (2 * m)) * sum((1:n > 1) * (theta .^ 2));

for i = 1:size(theta),
    grad(i) = (1 / m) * sum((hth - y) .* X(:, i)) + (i > 1) * (lambda / m) * theta(i);
end


% =========================================================================

grad = grad(:);

end
