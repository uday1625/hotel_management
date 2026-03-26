
document.addEventListener('DOMContentLoaded', function(){

  
  const roleSelect = document.getElementById('roleSelect');
  const adminFields = document.getElementById('adminFields');
  const userFields = document.getElementById('userFields');
  if(roleSelect){
    function updateRoleFields(){
      if(roleSelect.value === 'admin'){
        adminFields.style.display = 'block';
        userFields.style.display = 'none';
       
        const u = document.getElementById('username'); if(u) u.required = true;
        const p = document.getElementById('password'); if(p) p.required = true;
        const e = document.getElementById('email'); if(e) e.required = false;
        const ph = document.getElementById('phone'); if(ph) ph.required = false;
      } else {
        adminFields.style.display = 'none';
        userFields.style.display = 'block';
        const u = document.getElementById('username'); if(u) u.required = false;
        const p = document.getElementById('password'); if(p) p.required = false;
        const e = document.getElementById('email'); if(e) e.required = true;
        const ph = document.getElementById('phone'); if(ph) ph.required = true;
      }
    }
    updateRoleFields();
    roleSelect.addEventListener('change', updateRoleFields);
  }

  
  const captchaExprEl = document.getElementById('captchaExpr');
  const captchaAnsEl = document.getElementById('captchaAns');
  if(captchaExprEl && captchaAnsEl){
    const a = Math.floor(Math.random()*9) + 1;
    const b = Math.floor(Math.random()*9) + 1;
    const opList = ['+','-','*'];
    const op = opList[Math.floor(Math.random()*opList.length)];
    const expr = `${a} ${op} ${b}`;
    
    let ans = 0;
    if(op === '+') ans = a + b;
    if(op === '-') ans = a - b;
    if(op === '*') ans = a * b;
    captchaExprEl.innerText = expr + ' = ?';
    captchaAnsEl.value = ans;
  }

  
  const loginForm = document.getElementById('loginForm');
  if(loginForm){
    loginForm.addEventListener('submit', function(e){
      const userAns = document.getElementById('captchaInput')?.value;
      const real = document.getElementById('captchaAns')?.value;
      if(String(userAns).trim() !== String(real).trim()){
        e.preventDefault();
        alert('Captcha incorrect. Please try again.');
      }
    });
  }

});