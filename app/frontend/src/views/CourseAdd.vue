<template>
  <div class="home">
	<RegisterForm></RegisterForm>
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
};
</script>
