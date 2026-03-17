# 🎬 Kybernis 900-Second Demo: The "Bleeding Neck" Tutorial Script

**Goal:** Prove that standard idempotency keys fail against LLM agents, and position Kybernis Audit as the ultimate vulnerability scanner.
**Starting Point:** A fresh clone of Google's `adk-samples/typescript/agents/customer_service/customer_service`.

---

## 🛑 0:00 - The Hook (Intro)
**[ACTION: Screen shows the standard Cymbal Customer Service agent code (`prompts.ts`, `tools.ts`).]**

**[VOICEOVER]**
"If you are building AI agents with standard frameworks like LangChain or the Google ADK, your infrastructure is vulnerable to Semantic Double-Spends. LLMs are intentionally stateless. Today, I'm going to show you why standard backend idempotency keys won't save you, and how to fuzz your agent's tools using the open-source Kybernis Audit engine."

---

## 🛠️ 1:00 - Step 1: Building the Target Backend
**[ACTION: Create a new file called `cymbal_backend.ts` in your editor. Type/Paste the following code, explaining line-by-line.]**

```typescript
import * as http from 'http';

// 1. We set up an in-memory database for our planting service bookings.
const bookings = new Set<string>();
const idempotencyCache = new Set<string>();

const server = http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/api/schedule_planting') {
    let body = '';
    req.on('data', chunk => { body += chunk.toString(); });
    req.on('end', () => {
      const payload = JSON.parse(body);
      const idempotencyKey = payload.idempotency_key;

      console.log(`\n[API INBOUND] Request received for customer ${payload.customer_id}`);

      // 2. THE COMMUNITY MITIGATION: We check if we've seen this idempotency key before.
      // If the agent got stuck in a loop and retried the exact same payload, we block it.
      if (idempotencyKey && idempotencyCache.has(idempotencyKey)) {
        console.log(`[API GATEWAY] 🛡️ Duplicate caught! Idempotency key ${idempotencyKey} already processed.`);
        res.writeHead(200);
        return res.end(JSON.stringify({ status: 'ignored' }));
      }

      // 3. THE EXECUTION: We book the service and cache the key.
      const bookingString = `${payload.customer_id}-${payload.date}-${payload.time_slot}`;
      bookings.add(bookingString);
      if (idempotencyKey) idempotencyCache.add(idempotencyKey);

      console.log(`[DATABASE] 🌺 ACTION EXECUTED: Scheduled Planting for ${bookingString}`);
      console.log(`[DATABASE] Total Bookings for this slot: ${Array.from(bookings).filter(b => b === bookingString).length}`);
      
      res.writeHead(200);
      res.end(JSON.stringify({ status: 'success' }));
    });
  }
});

server.listen(3000, () => console.log('🌱 Cymbal API listening on port 3000\n   Mitigations: ✅ Idempotency Keys\n'));
```

**[VOICEOVER]**
"This is a standard Node backend. We did what the forums told us: we implemented an Idempotency Cache. Let's start the server."

**[ACTION: Open terminal 1 and run:]**
`npx ts-node cymbal_backend.ts`

---

## 🛡️ 3:00 - Step 2: The False Sense of Security (DARE Attack)
**[ACTION: Open terminal 2. Create `scenario.yaml` in the editor.]**

**[VOICEOVER]**
"Now, we use `kybernis-audit`, our open-source agent fuzzer. We define our target tool, the payload, and our first attack vector: **DARE** (Duplicate Action Replay). This simulates an agent that timed out and blindly retried the exact same request."

```yaml
name: "Cymbal Planting Service Fuzzing"
target_url: "http://localhost:3000/api/schedule_planting"
payload:
  customer_id: "123"
  date: "2026-04-01"
  time_slot: "09:00 AM"
idempotency_key_path: "idempotency_key"
delay_ms: 1000

attack_vector: "dare"
variant: "immediate"
```

**[ACTION: Run the fuzzer in Terminal 2]**
`kybernis-audit fuzz --config scenario.yaml`

**[VOICEOVER]**
"Watch what happens. The fuzzer fires the baseline request. The backend processes it. Then the fuzzer simulates the blind retry. 
*(Highlight the output)* 
Look at our backend terminal: `Duplicate caught!`. And Kybernis Audit outputs: `✅ [PASSED] Backend caught the duplicate payload`. We feel safe. But we aren't."

---

## 🩸 6:00 - Step 3: The Kill Shot (DRIFT Attack)
**[ACTION: Go back to `scenario.yaml` in the editor. Change the bottom two lines.]**

```yaml
attack_vector: "drift"
variant: "hash_bypass"
```

**[VOICEOVER]**
"Agents are not deterministic scripts. They are stateless LLMs. When they retry, they hallucinate. They generate new UUIDs, or they change the reasoning string in the JSON payload. This is called Semantic Drift. Let's see if our idempotency keys survive a **DRIFT** attack with a hash bypass."

**[ACTION: Run the fuzzer again in Terminal 2]**
`kybernis-audit fuzz --config scenario.yaml`

**[VOICEOVER]**
"The fuzzer fires the baseline. But on the retry, it injects a hallucinated reasoning string, simulating the LLM altering the payload. 
*(Point to the blood-red terminal output)*
**FAILED: Backend is bleeding. Semantic double-spend executed.**
Look at our database: `Total Bookings for this slot: 2`. We just double-booked the gardener."

---

## 📚 9:00 - Step 4: The Report & The Fix
**[ACTION: Scroll up in the fuzzer terminal to show the mitigation block.]**

**[VOICEOVER]**
"Kybernis Audit doesn't just break your code; it tells you why the community mitigations fail. It pulls real-world case studies—like the Air Canada Bereavement Fare disaster—where payload drift bypassed backend constraints. 

Hashing the payload doesn't work when the LLM coerces an integer to a float or adds a space. Generating UUIDs locally doesn't work when the LLM forgets the UUID and makes a new one on retry."

**[ACTION: Switch to browser showing kybernis.dev or the Kybernis SDK GitHub repo]**

**[VOICEOVER]**
"The only way to solve this is to stop trusting the LLM's memory. You need an external State-Machine Architecture.
With the Kybernis SDK, you wrap your tool execution in two lines of code. We anchor the agent to a persistent Session ID and engage a pessimistic Semantic Lock. No matter how much the LLM hallucinates or drifts, the infrastructure catches the intent and blocks the double-spend natively.

Diagnose the disease for free with Kybernis Audit. Sell the surgery with the Kybernis SDK. Link in the description."
