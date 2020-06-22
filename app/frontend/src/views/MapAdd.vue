<template>
  <div class="home">
    <AddMapForm @mapadd="validate">
    </AddMapForm>
  </div>
</template>

<script>
// @ is an alias to /src
import AddMapForm from '@/components/AddMap.vue';

export default {
  name: 'AddMap',
  components: {
    AddMapForm,
  },
  methods: {
    validate(newmap) {
      alert(newmap);
    },
  },
};
</script>
