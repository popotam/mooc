function [J, grad] = costFunctionReg(theta, X, y, lambda)
%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

% Initialize some useful values
m = length(y); % number of training examples
n = size(theta, 1);

% You need to return the following variables correctly 
J = 0;
grad = zeros(n, 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta

bad_eye = eye(n, n);
bad_eye(1,1) = 0;

hth = sigmoid(X * theta);  % vector
J = (1 / m) * sum(-y .* log(hth) - (1 - y) .* log(1 - hth)) + (lambda / (2*m)) * sum(bad_eye * theta .^ 2);

for i = 1:size(theta),
    grad(i) = (1 / m) * sum((hth - y) .* X(:, i)) + (i > 1) * lambda * theta(i) / m;
end

% =============================================================

end
