function [J,U]=ValueIteration

% DEFINE GLOBAL PARAMETERS
global res xdim ydim nx ny dx dy perr vGoal vObst vMove vInitial
% - minimum grid resolution
res = 0.15;
% - dimensions of the world
xdim = [-1.45 1.45];
ydim = [-0.6 0.6];
% - number of grid cells
nx=ceil((xdim(2)-xdim(1))/res);
ny=ceil((ydim(2)-ydim(1))/res);
% - size of grid cells
dx = (xdim(2)-xdim(1))/nx;
dy = (ydim(2)-ydim(1))/ny;
% - probability of going the wrong way
perr = 0.1;
% - value of goal, collision, movement
vGoal = 100;
vObst = -100;
vMove = -1;
% - initial guess at all values
vInitial = 0;

% DEFINE OBSTACLE AND GOAL LOCATIONS
obst = [1:nx 1:nx; ones(1,nx) ny*ones(1,nx)];
obst = [obst [ones(1,ny) nx*ones(1,ny); 1:ny 1:ny]];
obst = [obst [5:(nx-4); 2*ones(size(5:(nx-4)))]];
obst = [obst [5:(nx-4); 4*ones(size(5:(nx-4)))]];
isobst=sparse(zeros(nx,ny));
for k=1:size(obst,2)
    isobst(obst(1,k),obst(2,k))=1;
end
isgoal=sparse(zeros(nx,ny));
isgoal(3,3)=1;

% DEFINE INITIAL GUESS AT VALUE AND POLICY
for i=1:nx
    for j=1:ny
        if (isobst(i,j))
            J(i,j) = vObst;
            U(i,j) = 0;
        elseif (isgoal(i,j))
            J(i,j) = vGoal;
            U(i,j) = 0;
        else
            J(i,j) = vInitial;
            U(i,j) = ceil(4*rand);
        end
    end
end

% SETUP FIGURE
[Hcolor,Hcost,Haction]=setupfigure(isobst,isgoal,J);

% DO VALUE ITERATION
uchange(1)=0;
Jsto=reshape(J,[],1);
T=100;
for t=2:T
    % Uncomment one of these things to slow the display down.
%     pause;
%     pause(0.1);
    drawnow;
    
    % Iterate over all states.
    Jprev = J;
    Uprev = U;
    uchange(t)=0;
    for i=1:nx
        for j=1:ny
            % Update the value/policy for every square that is not an
            % obstacle and not a goal.
            if ((~isgoal(i,j)) & (~isobst(i,j)))
                % Get the old expected cost-to-go from the squares to the
                % north, south, east, and west.
                cn = Jprev(i,j+1);
                cs = Jprev(i,j-1);
                ce = Jprev(i+1,j);
                cw = Jprev(i-1,j);
                
                % Now compute the total expected cost for each of the four
                % possible actions (north, south, east, west).
                Jn = -1+((1-perr)*cn + (perr/2)*ce + (perr/2)*cw);
                Js = -1+((1-perr)*cs + (perr/2)*ce + (perr/2)*cw);
                Je = -1+((1-perr)*ce + (perr/2)*cn + (perr/2)*cs);
                Jw = -1+((1-perr)*cw + (perr/2)*cn + (perr/2)*cs);
                
                % Finally compute the new expected cost-to-go, by taking
                % the maximum over possible actions. Note when I say
                % "cost-to-go" here, I really mean "payoff-to-go". Also
                % note that actions are denoted 1=north, 2=south, 3=east,
                % and 4=west.
                [J(i,j),U(i,j)] = max([Jn Js Je Jw]);
                
                % See if the policy changed (for display purposes only).
                if (U(i,j)~=Uprev(i,j))
                    uchange(t) = uchange(t)+1;
                end
            end
        end
    end
    % Record the values (for display purposes only).
    Jsto=[Jsto reshape(J,[],1)];
    
    % Update the display.
    updatefigure(Hcolor,Hcost,Haction,J,U,Uprev,t);
end

% DISPLAY THE RESULTS (HOW THE VALUES/POLICY CHANGE AT EACH ITERATION)
displayresults(T,Jsto,uchange);



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% FUNCTIONS FOR DISPLAY (SHOULD BE ABLE TO SAFELY IGNORE THESE)


function [Hcolor,Hcost,Haction]=setupfigure(isobst,isgoal,J)
global res xdim ydim nx ny dx dy

% SETUP THE FIGURE
figure(1);
clf;
axis equal;
axis([xdim ydim]);
set(gca,'xtick',[],'ytick',[]);
set(gca,'layer','top');
box on;
hold on;

% DRAW HORIZONTAL AND VERTICAL GRID LINES
for i=1:nx-1
    h=line((xdim(1)+(i/nx)*(xdim(2)-xdim(1)))*[1 1],ydim);
    set(h,'color',0.8*ones(1,3));
end
for i=1:ny-1
    h=line(xdim,(ydim(1)+(i/ny)*(ydim(2)-ydim(1)))*[1 1]);
    set(h,'color',0.8*ones(1,3));
end

% COLOR THE SQUARES
for i=1:nx
    for j=1:ny
        if isgoal(i,j)
            Hcolor(i,j)=colorsquare(i,j,'g');
        elseif isobst(i,j)
            Hcolor(i,j)=colorsquare(i,j,'k');
        else
            Hcolor(i,j)=colorsquare(i,j,'w');
        end
        Hcost(i,j)=labelsquare(i,j,sprintf('%.1f',J(i,j)));
        Haction(i,j)=actionsquare(i,j);
    end
end

function updatefigure(Hcolor,Hcost,Haction,J,U,Uprev,t)
global nx ny
for i=1:nx
    for j=1:ny
        set(Hcost(i,j),'string',sprintf('%.0f',J(i,j)));
        reactionsquare(i,j,U(i,j),Haction(i,j));
        if (U(i,j)~=Uprev(i,j))
            set(Hcolor(i,j),'facecolor','y');
        else
            ccur = get(Hcolor(i,j),'facecolor');
            if (ccur==[1 1 0])
                set(Hcolor(i,j),'facecolor','w');
            end
        end
    end
end
title(sprintf('iter=%d',t));

% function displayresults(T,Jsto,uchange)
% global nx ny
% figure(2);
% clf;
% hold on;
% plot(1:T,Jsto,'k-');
% for t=1:T
%     if uchange(t)
%         h=line([t t],[-100 -100+(200*uchange(t)/(nx*ny))]);
%         set(h,'color','r','linewidth',2);
%     end
% end
% title(sprintf('Last change at iteration %d',find(uchange,1,'last')));

function marksquare(i,j)
colorsquare(i,j,'k');

function h=colorsquare(i,j,c,h)
global res xdim ydim nx ny dx dy
x = xdim(1)+((i-1)*dx);
y = ydim(1)+((j-1)*dy);
h=rectangle('position',[x y dx dy],'facecolor',c,'edgecolor',0.8*ones(1,3));

function h=labelsquare(i,j,s)
global res xdim ydim nx ny dx dy
x = xdim(1)+((i+0.5-1)*dx);
y = ydim(1)+((j+0.5-1)*dy);
h=text(x,y,s);
set(h,'fontsize',12,'color','r','horizontalalignment','center');

function h=actionsquare(i,j)
global res xdim ydim nx ny dx dy
x = xdim(1)+((i+0.5-1)*dx);
y = ydim(1)+((j+0.5-1)*dy);
h = line([x x],[y y]);
set(h,'color','b','linewidth',2);

function reactionsquare(i,j,d,h)
global res xdim ydim nx ny dx dy
x = xdim(1)+((i+0.5-1)*dx);
y = ydim(1)+((j+0.5-1)*dy);
if (d~=0)
    D = [0 dy; 0 -dy; dx 0; -dx 0]';
    set(h,'xdata',x+D(1,d)*[0.35 0.45],'ydata',y+D(2,d)*[0.35 0.45]);
end
