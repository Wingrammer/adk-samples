import * as http from 'http';

// In-memory database representing the Cymbal Home & Garden booking system
const bookings = new Set<string>();
const idempotencyCache = new Set<string>();

const server = http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/api/schedule_planting') {
    let body = '';
    req.on('data', chunk => { body += chunk.toString(); });
    req.on('end', () => {
      try {
        const payload = JSON.parse(body);
        const idempotencyKey = payload.idempotency_key;

        console.log(`\n[API INBOUND] Request received for customer ${payload.customer_id}`);

        // 🤝 COMMUNITY MITIGATION: Standard Idempotency Key Check
        // If the agent sends the exact same key, we safely ignore the duplicate.
        if (idempotencyKey && idempotencyCache.has(idempotencyKey)) {
          console.log(`[API GATEWAY] 🛡️ Duplicate caught! Idempotency key ${idempotencyKey} already processed.`);
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ status: 'ignored', message: 'Duplicate safely ignored.' }));
          return;
        }

        // ⚠️ VULNERABILITY: No semantic execution lock (Kybernis missing)
        // If the ID changes (DRIFT) but it's the same time and customer, we double-book.
        const bookingString = `${payload.customer_id}-${payload.date}-${payload.time_slot}`;
        
        bookings.add(bookingString);
        if (idempotencyKey) {
          idempotencyCache.add(idempotencyKey);
        }

        console.log(`[DATABASE] 🌺 ACTION EXECUTED: Scheduled Planting for ${bookingString}`);
        console.log(`[DATABASE] Total Bookings for this slot: ${Array.from(bookings).filter(b => b === bookingString).length}`);
        
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'success', booking_id: 'BKG-' + Math.floor(Math.random() * 10000) }));
      } catch (e) {
        res.writeHead(400);
        res.end();
      }
    });
  } else {
    res.writeHead(404);
    res.end();
  }
});

server.listen(3000, () => {
  console.log('🌱 Cymbal Backend API listening on port 3000');
  console.log('   Endpoint: POST /api/schedule_planting');
  console.log('   Mitigations Active: ✅ Idempotency Keys');
  console.log('   Mitigations Missing: ❌ Kybernis Semantic Lock\n');
});
