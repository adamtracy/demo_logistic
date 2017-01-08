

// I'm in charge of x, y scaling and render the axes
function Graph(display_opts) {
    this.opts = display_opts;

    this.invert = function(attr) {
        this.opts.r_min = this.xScale.invert(attr.x1);
        this.opts.r_max = this.xScale.invert(attr.x2);
        this.opts.x_min = this.yScale.invert(attr.y2);
        this.opts.x_max = this.yScale.invert(attr.y1);
    }

    this.r_min = function() { return this.opts.r_min; }
    this.r_max = function() { return this.opts.r_max; }
    this.x_min = function() { return this.opts.x_min; }
    this.x_max = function() { return this.opts.x_max; }
    this.h = function() { return this.opts.h; }
    this.w = function() { return this.opts.w; }
    this.padding = function() { return this.opts.padding; }


     // normally if you hadn't apriori knowledge of the domain, you'd be able to derive it using
     // some d3.min or d3.max() but luckily we don't have to know this.
     this.initScales = function() {
         this.xScale = d3.scale.linear()
                        .nice()
                         .domain([this.r_min(), this.r_max()])
                         .range([this.padding(), this.w() - this.padding()]);

        this.yScale = d3.scale.linear()
                        .nice()
                         .domain([this.x_min(), this.x_max()])
                         .range([this.h() - this.padding(), this.padding()]);
    }
    this.draw = function() {
        this.initScales()
        d3.select("svg").remove();
        var svg = d3.select("#content")
            .append("svg");
        svg.attr("id", "plot")

        svg.attr("width", this.w())
            .attr("height", this.h());

        var xAxis = d3.svg.axis()
                        .scale(this.xScale)
                        .orient("bottom");

        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(0," + (this.h() - this.padding()) + ")")
            .call(xAxis);

        var yAxis = d3.svg.axis()
                  .scale(this.yScale)
                  .orient("left");
        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(" + (this.padding() + 10) + ", 0)")
            .call(yAxis);
    }
};

function StretchRect(svg, xScale, yScale) {
    // I  keep track of the current selection rubber band region in the display.
    this.xScale = xScale;
    this.yScale = yScale;
    this.svg = svg;
	this.rect = null;
	this.prevRect = null;
	this.currentY = 0;
	this.currentX = 0;
	this.originX = 0;
	this.originY = 0;

	this.setRect = function(element) {
		this.prevRect = this.rect;
		this.rect = element;
	};

	this.getNewAttributes = function() {
		var x = this.currentX < this.originX? this.currentX:this.originX;
		var y = this.currentY < this.originY? this.currentY:this.originY;
		var width = Math.abs(this.currentX - this.originX);
		var height = Math.abs(this.currentY - this.originY);
		return {
	        x: x,
	        y: y,
	        width: width,
	        height: height
		};
	};

	this.getCurrentAttributes = function() {
		// use plus sign to convert string into number
		var x = + this.rect.attr("x");
		var y = + this.rect.attr("y");
		var width = + this.rect.attr("width");
		var height = + this.rect.attr("height");
		return {
			x1: x,
	        y1: y,
	        x2: x + width,
	        y2: y + height
		};
	};

	this.getCurrentAttributesAsText = function() {
		var attrs = this.getCurrentAttributes();
		return "x1: " + xScale.invert(attrs.x1)
		   + " x2: " + xScale.invert(attrs.x2)
		   + " y1: " + yScale.invert(attrs.y1)
		   + " y2: " + yScale.invert(attrs.y2);
	};

	this.init = function(newX, newY) {
		var rectElement = this.svg.append("rect")
		    .attr({
		        x: 0,
		        y: 0,
		        width: 0,
		        height: 0
		    })
		    .classed("selection", true);
	    this.setRect(rectElement);
		this.originX = newX;
		this.originY = newY;
		this.update(newX, newY);
	};

	this.update = function(newX, newY) {
		this.currentX = newX;
		this.currentY = newY;
		this.rect.attr(this.getNewAttributes());
	};

	this.focus = function() {
        this.rect
            .style("stroke", "#DE695B")
            .style("stroke-width", "2.5");
    };

    this.remove = function() {
    	this.rect.remove();
    	this.rect = null;
    };

    this.removePrevious = function() {
    	if(this.prevRect) {
    		this.prevRect.remove();
    	}
    };

};

function render(dataset, graph) {
    var svg = d3.select("#plot")
    var xScale = graph.xScale;
    var yScale = graph.yScale;
    svg.selectAll("circle")
        .data(dataset)
        .enter()
        .append("circle")
        .attr("cx", function(d) {
            return xScale(d[0]);
        })
        .attr("cy", function(d) {
            return yScale(d[1]);
         })
        .attr("r", 1);

    // Now set up the selection rectangle for zooming into the dataset
    selectionRect = new StretchRect(svg, xScale, yScale);
    // these are callbacks for dragging event activity
    function dragStart() {
        var p = d3.mouse(this);
        selectionRect.init(p[0], p[1]);
        selectionRect.removePrevious();
    }

    function dragMove() {
        var p = d3.mouse(this);
        selectionRect.update(p[0], p[1]);
        d3.select("#attributestext")
            .text(selectionRect.getCurrentAttributesAsText());
    }

    function dragEnd() {
        console.log("dragEnd");
        var finalAttributes = selectionRect.getCurrentAttributes();
        console.dir(finalAttributes);
        if(finalAttributes.x2 - finalAttributes.x1 > 1 && finalAttributes.y2 - finalAttributes.y1 > 1){
            console.log("range selected");
            // range selected
            d3.event.sourceEvent.preventDefault();
            selectionRect.focus();
            var attrs = selectionRect.getCurrentAttributes();
            /*
            graph.r_min=xScale.invert(attrs.x1);
            graph.r_max=xScale.invert(attrs.x2);
            graph.x_min=yScale.invert(attrs.y1);
            graph.x_max=yScale.invert(attrs.y2);
            */
            graph.invert(attrs);
            graph.draw();
            var target = document.getElementById('content');
            var spinner = new Spinner(spinner_opts).spin(target);
            d3.json('/logistic/'+graph.r_min()+'/'+graph.r_max()+'/'+graph.x_min()+'/'+graph.x_max(),
                function(json){render(json, graph); spinner.stop();} );

        } else {
            // null selection
            selectionRect.remove();
        }
    }

    var dragBehavior = d3.behavior.drag()
        .on("drag", dragMove)
        .on("dragstart", dragStart)
        .on("dragend", dragEnd);

    svg.call(dragBehavior);

};

// global starting points here
/*
var r_min = 2.5;
var r_max = 4.0001;
var x_min = 0;
var x_max = 1;
*/

// options for spinner which is engaged while the back
// end chooches over the data (http://spin.js.org/)
var spinner_opts = {
  lines: 7 // The number of lines to draw
, length: 18 // The length of each line
, width: 14 // The line thickness
, radius: 42 // The radius of the inner circle
, scale: 1 // Scales overall size of the spinner
, corners: 1 // Corner roundness (0..1)
, color: '#000' // #rgb or #rrggbb or array of colors
, opacity: 0.25 // Opacity of the lines
, rotate: 0 // The rotation offset
, direction: 1 // 1: clockwise, -1: counterclockwise
, speed: 1 // Rounds per second
, trail: 60 // Afterglow percentage
, fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
, zIndex: 2e9 // The z-index (defaults to 2000000000)
, className: 'spinner' // The CSS class to assign to the spinner
, top: '50%' // Top position relative to parent
, left: '50%' // Left position relative to parent
, shadow: false // Whether to render a shadow
, hwaccel: false // Whether to use hardware acceleration
, position: 'absolute' // Element positioning
};

var display_opts = {
    r_min: 2.5,
    r_max: 4.0001,
    x_min: 0.0001,
    x_max: 1.0001,
    w: 900,
    h: 400,
    padding: 20,
    AR: 0.44
};

//graph = new Graph(r_min, r_max, x_min, x_max)
var graph = new Graph(display_opts);



graph.draw();
var target = document.getElementById('content');
var spinner = new Spinner(spinner_opts).spin(target);
d3.json('/logistic/'+display_opts.r_min+'/'+display_opts.r_max +'/'+display_opts.x_min+'/'+display_opts.x_max, function(json){render(json, graph); spinner.stop()} );

