<template>
  <div class="home">
    <RegisterForm v-on:submit.prevent="validate" v-bind:roles="roles" v-bind:depts="depts"></RegisterForm>
  </div>
</template>

<script>
// @ is an alias to /src
import RegisterForm from '@/components/RegisterUser.vue';

export default {
  name: 'Reg',
  components: {
    RegisterForm,
  },
  data() {
    return {
      roles: [{ id: 1, name: 'Student' }, { id: 2, name: 'Prof' }, { id: 3, name: 'TA' }, { id: 4, name: 'Admin' }],
      depts: [{ id: 1, name: 'CSE' }, { id: 2, name: 'ECE' }],
    };
  },
  methods: {
    validate(newuser) {
      const t = 7;
      console.log(t);
    },
  },
};
</script>
