<template>
 <div>
    {{ user.username }}
    {{ user.email }}
    {{ user.dept }}
    {{ user.role }}
    <button @click="deleterec"> Delete </button>
    <button @click="updaterec"> Update </button>
 </div>
</template>

<script>
export default {
  name: 'UserRecord',
  props: { user: Array },
  methods: {
    updaterec() {
      this.$emit('updrec', this.user);
    },
    deleterec() {
      this.$emit('delrec', this.user);
    },
  },
};
</script>
