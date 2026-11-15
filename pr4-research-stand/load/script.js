import http from 'k6/http';
import { check } from 'k6';
// Замкнутая модель: USERS виртуальных пользователей без пауз
export const options = { vus: Number(__ENV.USERS || 50), duration: `${__ENV.SECONDS || 60}s` };
export default function () {
  const r = http.get(`${__ENV.HOST || 'http://sut:8000'}/api/items/42`);
  check(r, { 'status 200': (x) => x.status === 200 });
}
