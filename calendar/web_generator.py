#The purpose of this file is to generate the big html file which we are having in the end

week_names=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
id_list1=[0,1,3]
id_list2=[0,1,3]


file = open('out.html', 'w')


def initialization():
	#Header Lines
	file.write("""   
	<!DOCTYPE html>
	<html lang="en">
	<head>
	  <title>Bootstrap Example</title>
	  <meta charset="utf-8">
	  <meta name="viewport" content="width=device-width, initial-scale=1">
	  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
	  <link rel="stylesheet" type="text/css" href="calendar.css"/>
	  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
	  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>"
	  
	</head>
	""")


	#Jumbotrone + Navigation bar

	file.write("""
	<body>	
	    <div class="jumbotron">
    		<div class="container text-center">
      		<h2>Larkstaden's Studiecentrum</h2>      
    		</div>
  		</div>
	  <nav class="navbar navbar-inverse">
		<div class="container-fluid">
		  <div class="navbar-header">
			<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
			  <span class="icon-bar"></span>
			  <span class="icon-bar"></span>
			  <span class="icon-bar"></span>						
			</button>
			<a class="navbar-brand" href="#">Logo</a>
		  </div>
		  <div class="collapse navbar-collapse" id="myNavbar">
			<ul class="nav navbar-nav">
			  <li class="active"><a href="#">Home</a></li>
			  <li><a href="#">Products</a></li>
			  <li><a href="#">Deals</a></li>
			  <li><a href="#">Stores</a></li>
			  <li><a href="#">Contact</a></li>
			</ul>
			<ul class="nav navbar-nav navbar-right">
			  <li><a href="#"><span class="glyphicon glyphicon-user"></span> Your Account</a></li>
			  <li><a href="#"><span class="glyphicon glyphicon-shopping-cart"></span> Cart</a></li>
			</ul>
		  </div>
		</div>
	  </nav>
	""")







def print_week(id_list): #pass list of lists with ids 
	#prints First row tag + weather widget
	file.write("""<div class="container">
					<div class="row">""")
	file.write("""
			<div class="col-sm-3"> 
			 

						<a href="http://www.accuweather.com/en/se/stockholm/314929/weather-forecast/314929" class="aw-widget-legal">
						</a><div id="awcc1461059257967" class="aw-widget-current"  data-locationkey="314929" data-unit="c" data-language="en-us" data-useip="false" data-uid="awcc1461059257967"></div><script type="text/javascript" src="http://oap.accuweather.com/launch.js"></script>
			  
			</div>
			""")
	for i in range(7):
		if week_names[i]=="Thursday":
			file.write("""
					  </div>
					</div><br>

					<div class="container">	
						  <div class="row">	
					  """)
			

		file.write("""
			 <div class="col-sm-3">
			  <div class="panel panel-primary">
				<div class="panel-heading">%s</div>
				<div class="panel-body">
				  <div class= "day">
					<form>
					  Breakfast
					  <select name="breakfast">
						<option value="normal">Normal</option>
						<option value="early">Early</option>
					  </select>
					  <br>
					  Lunch
					  <select name="lunch">
						<option value="normal">Normal</option>
						<option value="lunchbox">lunchbox</option>
						<option value="sandwiches">sandwiches</option>
					  </select>
					  <br>
					  Dinner
					  <select name="lunch">
						<option value="normal">Normal</option>
						<option value="late_dinner">Late dinner</option>
						<option value="lunchbox">lunchbox</option>
						<option value="sandwiches">sandwiches</option>
					  </select>
					  <br>

					  <button class="btn btn-success btn-md">Comment</button>
					</form>
				  </div>
				</div>
				
			  </div>
			</div>
			  """  %(week_names[i]))

	file.write("""</div>
		</div><br><br>""")


def print_carousel():
	#Carousel initialization
	file.write("""
	  <div id="myCarousel" class="carousel slide" data-ride="carousel" data-interval="false">
		<div class="carousel-inner" role="listbox">
		  <div class="item active">
		""")
	print_week(id_list1)
	file.write("""</div>
		<div class="item">""")
	print_week(id_list2)
	file.write("""
					</div>
				</div>			
			 <a class="left carousel-control" href="#myCarousel" role="button" data-slide="prev">
			  <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
			  <span class="sr-only">Previous</span>
			</a>
			<a class="right carousel-control" href="#myCarousel" role="button" data-slide="next">
			  <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
			  <span class="sr-only">Next</span>
			</a>
		  </div>
		</div>
			<footer class="container-fluid text-center">
			  <p>Online Store Copyright</p>  
			  <form class="form-inline">Get deals:
				<input type="email" class="form-control" size="50" placeholder="Email Address">
				<button type="button" class="btn btn-danger">Sign Up</button>
			  </form>
			</footer>
			<script>

				$(document).ready(function(){
		    		$('.btn').popover({title: "<strong>Comment:</strong>", content: "<form><input type='text'/></form>", html: true, placement: "bottom"}); 
				});
	  		</script>

		</body>
		</html>""")

#"<input type="text" name="comment">"

initialization()
print_carousel()
file.close()





