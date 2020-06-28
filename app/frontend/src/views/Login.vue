<template>
  <div class="home">
    <LogForm @login="validate"></LogForm>
  </div>
</template>

<script>
// @ is an alias to /src
import LogForm from '@/components/LogForm.vue';
import axios from 'axios';

export default {
  name: 'Form',
  components: {
    LogForm,
  },
  methods: {
    validate(cred) {
      const path = 'http://localhost:5000/users/login';
      axios.post(path, cred)
        .then((res) => {
          alert(res.data.status);
        })
        .catch((res) => {
          console.log(res);
        });
    },
  },
};
</script>
