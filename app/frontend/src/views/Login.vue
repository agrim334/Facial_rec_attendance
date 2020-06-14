<template>
  <div class="home">
    <LogForm @userlogin="validate"></LogForm>
  </div>
</template>

<script>
// @ is an alias to /src
import LogForm from '@/components/LogForm.vue';

export default {
  name: 'Form',
  components: {
    LogForm,
  },
  methods: {
    validate(credentials) {
      if (credentials.user === null || credentials.user === '') {
        alert('Fill in user name');
      }
      if (credentials.pass === null || credentials.pass === '') {
        alert('Fill in password');
      }
    },
  },
};
</script>
