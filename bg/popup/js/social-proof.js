var customerFirst = ['Liam', 'Noah', 'William', 'James', 'Logan', 'Benjamin', 'Mason',
  'Elijah', 'Oliver', 'Jacob', 'Lucas', 'Michael', 'Alexander', 'Ethan', 'Daniel', 'Matthew',
  'Aiden', 'Henry', 'Joseph', 'Jackson', 'Samuel', 'Sebastian', 'David', 'Carter', 'Wyatt',
  'Jayden', 'John', 'Owen', 'Dylan', 'Luke', 'Gabriel', 'Anthony', 'Isaac', 'Grayson', 'Jack',
  'Julian', 'Levi', 'Christopher', 'Joshua', 'Andrew', 'Lincoln', 'Mateo', 'Ryan', 'Jaxon',
  'Nathan', 'Aaron', 'Isaiah', 'Thomas', 'Charles', 'Caleb', 'Josiah', 'Christian', 'Hunter',
  'Eli', 'Jonathan', 'Connor', 'Landon', 'Adrian', 'Asher', 'Cameron', 'Leo', 'Theodore',
  'Jeremiah', 'Hudson', 'Robert', 'Easton', 'Nolan', 'Nicholas', 'Ezra', 'Colton', 'Angel',
  'Brayden', 'Jordan', 'Dominic', 'Austin', 'Ian', 'Adam', 'Elias', 'Jaxson', 'Greyson',
  'Jose', 'Ezekiel', 'Carson', 'Evan', 'Maverick', 'Bryson', 'Jace', 'Cooper', 'Xavier',
  'Parker', 'Roman', 'Jason', 'Santiago', 'Chase', 'Sawyer', 'Gavin', 'Leonardo', 'Kayden',
  'Ayden', 'Jameson', 'Kevin', 'Bentley', 'Zachary', 'Everett', 'Axel', 'Tyler', 'Micah',
  'Vincent', 'Weston', 'Miles', 'Wesley', 'Nathaniel', 'Harrison', 'Brandon', 'Cole', 'Declan',
  'Luis', 'Braxton', 'Damian', 'Silas', 'Tristan', 'Ryder', 'Bennett', 'George', 'Emmett',
  'Justin', 'Kai', 'Max', 'Diego', 'Luca', 'Ryker', 'Carlos', 'Maxwell', 'Kingston', 'Ivan',
  'Maddox', 'Juan', 'Ashton', 'Jayce', 'Rowan', 'Kaiden', 'Giovanni', 'Eric', 'Calvin',
  'Abel', 'King', 'Camden', 'Amir', 'Blake', 'Alex', 'Brody', 'Malachi', 'Emmanuel', 'Jonah',
  'Beau', 'Jude', 'Antonio', 'Alan', 'Elliott', 'Elliot', 'Waylon', 'Xander', 'Timothy',
  'Victor', 'Bryce', 'Finn', 'Brantley', 'Edward', 'Abraham', 'Patrick', 'Marcus', 'Derek',
  'Craig', 'Raymond', 'Harold', 'Frank', 'Scott', 'Greg', 'Peter', 'Ralph', 'Keith', 'Todd',
  'Bruce', 'Gerald', 'Dennis', 'Roger', 'Wayne', 'Roy', 'Eugene', 'Russell', 'Larry', 'Philip',
  'Howard', 'Carl', 'Arthur', 'Albert', 'Randy', 'Barry', 'Glenn', 'Dale', 'Steve', 'Terry'
];
var customerLast = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
  'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
];
var customerStates = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',
  'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
  'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
  'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
];
var spBase = window.socialProofBase || '';
var customerProducts = [
  { quantity: '1', image: spBase + 'Images/1-bottles-vigor.webp', label: '1' },
  { quantity: '1', image: spBase + 'Images/1-bottles-vigor.webp', label: '1' },
  { quantity: '1', image: spBase + 'Images/1-bottles-vigor.webp', label: '1' },
  { quantity: '2', image: spBase + 'Images/2-bottles-vigor.webp', label: '2' },
  { quantity: '2', image: spBase + 'Images/2-bottles-vigor.webp', label: '2' },
  { quantity: '3', image: spBase + 'Images/3-bottles-vigor.webp', label: '3' },
  { quantity: '3', image: spBase + 'Images/3-bottles-vigor.webp', label: '3' },
  { quantity: '4', image: spBase + 'Images/4-bottles-vigor.webp', label: '4' },
  { quantity: '6', image: spBase + 'Images/6-bottles-vigor.webp', label: '6' },
  { quantity: '7', image: spBase + 'Images/7-bottles-vigor.webp', label: '7' }
];
function updateSocial() {
  var rCustomerFirst = customerFirst[Math.floor(Math.random() * customerFirst.length)];
  var rCustomerLast = customerLast[Math.floor(Math.random() * customerLast.length)];
  var rStates = customerStates[Math.floor(Math.random() * customerStates.length)];
  var rProduct = customerProducts[Math.floor(Math.random() * customerProducts.length)];
  var rAgo = Math.floor(Math.random() * 21) + 1;

  $('#notify-customer').html(rCustomerFirst + ' ' + rCustomerLast);
  $('#notify-state').html(rStates);
  $('#notify-quantity').html(rProduct.label);
  $('#notify-ago').html(rAgo + ' minutes ago');
  $('.custom-notification-image-wrapper img').attr('src', rProduct.image);
  if (rProduct.quantity > 1) {
    $('#notify-multiple').html('s');
  } else {
    $('#notify-multiple').html('');
  }
}

setInterval(function() {
  var  divID = $('.custom-social-proof');
  if (divID.is(':hidden')) {
    $('.custom-social-proof').stop().slideToggle('slow');
    updateSocial();
  } else {
    $(divID).stop().slideToggle('slow');
  }
}, 7000);

$('.custom-close').click(function() {
  $('.custom-social-proof').stop().slideToggle('slow');
});