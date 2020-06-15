<template>
  <div class="home">
    <RegisterForm @userreg="validate" :roles="roles" :depts="depts">
    </RegisterForm>
  </div>
</template>

<script>
// @ is an alias to /src
import RegisterForm from '@/components/RegisterUser.vue';

const validator = require('email-validator');

export default {
  name: 'Reg',
  components: {
    RegisterForm,
  },
  data() {
    return {
      roles: [{ id: 'r1', name: 'Student' }, { id: 'r2', name: 'Prof' }, { id: 'r3', name: 'TA' },
        { id: 'r4', name: 'Admin' }],
      depts: [{ id: 'd1', name: 'CSE' }, { id: 'd2', name: 'ECE' }],
    };
  },
  methods: {
    validate(newuser) {
      if (newuser.userid === null || newuser.userid === '') {
        alert('Fill in user name');
      }
      if (newuser.fname === null || newuser.fname === '') {
        alert('Fill in first name');
      }
      if (newuser.lname === null || newuser.lname === '') {
        alert('Fill in last name');
      }
      if (newuser.email === null || newuser.email === '') {
        alert('Fill in email');
      }
      if (validator.validate(newuser.email) === false) {
        alert('Email format is incorrect');
      }
      if (newuser.rolec === null || newuser.rolec === '') {
        alert('Choose a role');
      }
      if (newuser.deptc === null || newuser.deptc === '') {
        alert('Choose a department');
      }
      if (newuser.pass !== newuser.confirmpass) {
        alert('Password no match');
      }
    },
  },
};
</script>
