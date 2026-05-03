const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const { MongoClient, ObjectId } = require('mongodb');

const app = express();
const PORT = process.env.PORT || 3000;
const MONGO_URI = 'mongodb://root:example@localhost:27017/';
const DB_NAME = 'isl_dictionary';

let db;
let usersCollection;
let signsCollection;
let requestsCollection;

async function initDatabase() {
  const client = new MongoClient(MONGO_URI);
  await client.connect();
  console.log('Connected successfully to MongoDB server');
  
  db = client.db(DB_NAME);
  usersCollection = db.collection('users');
  signsCollection = db.collection('signs');
  requestsCollection = db.collection('requests');
  
  await usersCollection.createIndex({ username: 1 }, { unique: true });
  
  const signCount = await signsCollection.countDocuments();
  if (signCount === 0) {
    const sampleSigns = [
      { 
        word: 'Hello', 
        category: 'Greetings', 
        description: 'Raise hand to forehead, palm facing out, then move hand forward in a small wave motion.', 
        difficulty: 'Easy', 
        image_url: 'https://acetns.ie/wp-content/uploads/2017/05/lc3a1mh-hello.gif',
        status: 'approved', 
        created_at: new Date() 
      },
      { 
        word: 'Thank You', 
        category: 'Greetings', 
        description: 'Touch chin with fingertips, then move hand forward and down, palm facing up.', 
        difficulty: 'Easy', 
        image_url: 'https://risli.ie/app/uploads/2023/04/Picture1.jpg',
        status: 'approved', 
        created_at: new Date() 
      },
      { 
        word: 'Please', 
        category: 'Greetings', 
        description: 'Place flat hand on chest and make circular motion clockwise.', 
        difficulty: 'Easy', 
        image_url: 'https://res.cloudinary.com/spiralyze/image/upload/f_auto,w_auto/BabySignLanguage/DictionaryPages/please.svg',
        status: 'approved', 
        created_at: new Date() 
      },
      { 
        word: 'Family', 
        category: 'People', 
        description: 'Make two F handshapes with both hands, then move them in a circle to meet each other.', 
        difficulty: 'Medium', 
        image_url: '/images/family.png',
        status: 'approved', 
        created_at: new Date() 
      },
      { 
        word: 'Friend', 
        category: 'People', 
        description: 'Hook index fingers together and twist back and forth twice.', 
        difficulty: 'Easy', 
        image_url: 'https://www.british-sign.co.uk/british-sign-language/wp-content/uploads/2013/12/friend1-911x930.png',
        status: 'approved', 
        created_at: new Date() 
      },
      { 
        word: 'Help', 
        category: 'Actions', 
        description: 'Place one hand under the other fist, then lift both hands together upward.', 
        difficulty: 'Easy', 
        image_url: '/images/help.png',
        status: 'approved', 
        created_at: new Date() 
      },
      { 
        word: 'Book', 
        category: 'Education', 
        description: 'Place palms of your hands together infront of you, then open them like a book.Spread fingers on forehead, then close them into a fist while moving away from head.', 
        difficulty: 'Medium', 
        image_url: 'https://www.british-sign.co.uk/british-sign-language/wp-content/uploads/2013/03/book-661x930.png',
        status: 'approved', 
        created_at: new Date() 
      },
      { 
        word: 'Dictionary', 
        category: 'Education', 
        description: 'Place one hand out infront, palm up, followed by the other touching fingertips except the index which is pointed upwards.', 
        difficulty: 'Easy', 
        image_url: 'https://res.cloudinary.com/spiralyze/image/upload/f_auto,w_auto/BabySignLanguage/DictionaryPages/dictionary.svg',
        status: 'approved', 
        created_at: new Date() 
      },
      { 
        word: 'Water', 
        category: 'Food & Drink', 
        description: 'Make W handshape with three fingers, tap chin twice.', 
        difficulty: 'Easy', 
        image_url: 'https://res.cloudinary.com/spiralyze/image/upload/f_auto,w_auto/BabySignLanguage/DictionaryPages/water.svg',
        status: 'approved', 
        created_at: new Date() 
      },
      { 
        word: 'Ireland', 
        category: 'Places', 
        description: 'Make circular motions with both hands, representing the rolling hills of Ireland.', 
        difficulty: 'Medium', 
        image_url: '/images/ireland.png',
        status: 'approved', 
        created_at: new Date() 
      }
    ];
    await signsCollection.insertMany(sampleSigns);
    console.log('Sample ISL signs inserted');
  }
  
  const adminExists = await usersCollection.findOne({ username: 'admin' });
  if (!adminExists) {
    await usersCollection.insertOne({ 
      username: 'admin', 
      password: 'admin123', 
      role: 'admin',
      created_at: new Date()
    });
    console.log('Admin user created (username: admin, password: admin123)');
  }
}

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(session({
  secret: 'isl-secret-key-change-in-production',
  resave: false,
  saveUninitialized: false,
  cookie: { maxAge: 24 * 60 * 60 * 1000 }
}));

app.use(express.static('public'));

app.get('/api/signs', async (req, res) => {
  try {
    const signs = await signsCollection.find({ status: 'approved' }).toArray();
    res.json(signs);
  } catch (error) {
    console.error('Error fetching signs:', error);
    res.status(500).json({ error: 'Failed to fetch signs' });
  }
});

app.get('/api/signs/search', async (req, res) => {
  try {
    const { q, category, difficulty } = req.query;
    const query = { status: 'approved' };
    
    if (q) {
      query.$or = [
        { word: { $regex: q, $options: 'i' } },
        { description: { $regex: q, $options: 'i' } },
        { category: { $regex: q, $options: 'i' } }
      ];
    }
    if (category && category !== 'all') {
      query.category = category;
    }
    if (difficulty && difficulty !== 'all') {
      query.difficulty = difficulty;
    }
    
    const signs = await signsCollection.find(query).toArray();
    res.json(signs);
  } catch (error) {
    console.error('Error searching signs:', error);
    res.status(500).json({ error: 'Failed to search signs' });
  }
});

app.get('/api/signs/:id', async (req, res) => {
  try {
    const sign = await signsCollection.findOne({ _id: new ObjectId(req.params.id) });
    if (!sign) {
      return res.status(404).json({ error: 'Sign not found' });
    }
    res.json(sign);
  } catch (error) {
    console.error('Error fetching sign:', error);
    res.status(500).json({ error: 'Failed to fetch sign' });
  }
});

app.post('/api/requests', async (req, res) => {
  try {
    const { word, category, description, contributor_name, contributor_email } = req.body;
    
    if (!word || !category || !description || !contributor_name || !contributor_email) {
      return res.status(400).json({ error: 'All fields are required' });
    }
    
    const result = await requestsCollection.insertOne({
      word,
      category,
      description,
      contributor_name,
      contributor_email,
      status: 'pending',
      created_at: new Date()
    });
    
    res.json({ id: result.insertedId, message: 'Request submitted successfully' });
  } catch (error) {
    console.error('Error submitting request:', error);
    res.status(500).json({ error: 'Failed to submit request' });
  }
});

app.get('/api/requests', async (req, res) => {
  try {
    if (!req.session.userId || req.session.role !== 'admin') {
      return res.status(403).json({ error: 'Admin access required' });
    }
    
    const requests = await requestsCollection.find().sort({ created_at: -1 }).toArray();
    res.json(requests);
  } catch (error) {
    console.error('Error fetching requests:', error);
    res.status(500).json({ error: 'Failed to fetch requests' });
  }
});

app.post('/api/requests/:id/approve', async (req, res) => {
  try {
    if (!req.session.userId || req.session.role !== 'admin') {
      return res.status(403).json({ error: 'Admin access required' });
    }
    
    await requestsCollection.updateOne(
      { _id: new ObjectId(req.params.id) },
      { $set: { status: 'approved', approved_at: new Date() } }
    );
    res.json({ message: 'Request approved' });
  } catch (error) {
    console.error('Error approving request:', error);
    res.status(500).json({ error: 'Failed to approve request' });
  }
});

app.post('/api/requests/:id/reject', async (req, res) => {
  try {
    if (!req.session.userId || req.session.role !== 'admin') {
      return res.status(403).json({ error: 'Admin access required' });
    }
    
    await requestsCollection.updateOne(
      { _id: new ObjectId(req.params.id) },
      { $set: { status: 'rejected', rejected_at: new Date() } }
    );
    res.json({ message: 'Request rejected' });
  } catch (error) {
    console.error('Error rejecting request:', error);
    res.status(500).json({ error: 'Failed to reject request' });
  }
});

app.post('/api/register', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    if (!username || !password) {
      return res.status(400).json({ error: 'Username and password are required' });
    }
    
    if (password.length < 6) {
      return res.status(400).json({ error: 'Password must be at least 6 characters' });
    }
    
    await usersCollection.insertOne({ 
      username, 
      password: password, 
      role: 'user',
      created_at: new Date()
    });
    res.json({ message: 'User registered successfully' });
  } catch (error) {
    if (error.code === 11000) {
      res.status(400).json({ error: 'Username already exists' });
    } else {
      console.error('Error registering user:', error);
      res.status(500).json({ error: 'Failed to register user' });
    }
  }
});

app.post('/api/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    if (!username || !password) {
      return res.status(400).json({ error: 'Username and password are required' });
    }
    
    const user = await usersCollection.findOne({ username });
    
    if (!user || user.password !== password) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    req.session.userId = user._id.toString();
    req.session.username = user.username;
    req.session.role = user.role;
    res.json({ message: 'Logged in successfully', role: user.role, username: user.username });
  } catch (error) {
    console.error('Error logging in:', error);
    res.status(500).json({ error: 'Failed to login' });
  }
});

app.post('/api/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).json({ error: 'Failed to logout' });
    }
    res.json({ message: 'Logged out successfully' });
  });
});

app.get('/api/auth/status', (req, res) => {
  if (req.session.userId) {
    res.json({ 
      authenticated: true, 
      username: req.session.username,
      role: req.session.role 
    });
  } else {
    res.json({ authenticated: false });
  }
});

initDatabase().then(() => {
  app.listen(PORT, () => {
    console.log(`ISL Dictionary running on http://localhost:${PORT}`);
    console.log(`MongoDB Express UI: http://localhost:8081`);
  });
}).catch(err => {
  console.error('Failed to connect to MongoDB:', err);
  process.exit(1);
});
