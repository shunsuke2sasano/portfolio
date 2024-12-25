document.addEventListener('DOMContentLoaded', function () {
    const generalRadio = document.getElementById('generalRadio');
    const adminRadio = document.getElementById('adminRadio');
    const generalFields = document.getElementById('generalFields');
    const adminFields = document.getElementById('adminFields');

    // ラジオボタンの変更イベントでフォームを切り替え
    generalRadio.addEventListener('change', function () {
        if (this.checked) {
            generalFields.style.display = 'block';
            adminFields.style.display = 'none';
        }
    });

    adminRadio.addEventListener('change', function () {
        if (this.checked) {
            generalFields.style.display = 'none';
            adminFields.style.display = 'block';
        }
    });
});
