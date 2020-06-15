<template>
 <div>
  <table>
    <tbody>
      <tr v-for='user in users' :key='user.id'>
        <td>{{ user.id }}</td>
        <td>{{ user.username }}</td>
        <td>{{ user.email }}</td>
        <td>{{ user.dept }}</td>
        <td>{{ user.role }}</td>
      </tr>
    </tbody>
    <div>
      <button @click="add"> Add User </button>
    </div>
    <div>
      <button @click="deleteall"> Remove All records </button>
    </div>
  </table>
 </div>
</template>

<script>
export default {
  name: 'UserTable',
  data() {
    return { user: Array };
  },
  methods: {
    update(){
      console.log('dummy');
    }
    delete(){
      console.log('dummy');
    }
    add(){
      console.log('dummy');
    }
    deleteall(){
      console.log('dummy');
    }
  },
};
</script>
