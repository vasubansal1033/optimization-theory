clc;
clear;
% Parameters
N = 100; % No of iterations
x0 = [0 0]; % Initial point
epsilon1 = 0.0001;
epsilon2 = 0.0001;
k = 0;
% Define the function here
syms x y alpha;
f = (x^2+y-11)^2+(x+y^2-7)^2;

xk = x0; % xk is the current point
while k<=N
    % Calculate gradient
    g = gradient(f);
    
    grad = subs(g, [x y], xk);
    if norm(grad)<=epsilon1
        break
    else if k >= N
            break
        else
            fxnext = compose(f, xk-alpha*grad);
            alphamin = fminbnd(@fxnext,0,5);
            valNext = subs(fxnext, [alpha], alphamin);
            if dot(valNext, grad)<=epsilon2
                break
            end
            xnext = xk-alphamin*grad;
            if norm(xnext-xk)/norm(xk)<=epsilon1
                break
            else
                k=k+1;
                xk = xnext;
            end
        
            
        end
    end
end
