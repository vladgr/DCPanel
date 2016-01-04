import api.bm as models
from rest_framework import serializers


class ConfDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Conf


class ConfListSerializer(ConfDetailSerializer):
    class Meta(ConfDetailSerializer.Meta):
        exclude = ('data',)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country


class DbListSerializer(serializers.ModelSerializer):
    type_db_name = serializers.CharField(
        source='get_type_db_display', read_only=True)
    project_name = serializers.CharField(
        source='get_project_name', read_only=True)

    class Meta:
        model = models.Db
        fields = (
            'id',
            'server',
            'project',
            'project_name',
            'type',
            'type_db',
            'name',
            'version',
            'remote_access',
            'type_db_name'
        )


class DbDetailSerializer(DbListSerializer):
    """Field user is dict of users for server and single dict for project"""
    user = serializers.JSONField(source='get_user', read_only=True)
    server_ip = serializers.CharField(source='get_server_ip', read_only=True)

    class Meta(DbListSerializer.Meta):
        depth = 2
        fields = DbListSerializer.Meta.fields + ('user', 'server_ip')


class InstallSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Install


class IpSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ip


class PostfixEmailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(source='get_password', read_only=True)

    class Meta:
        model = models.PostfixEmail
        fields = ('email', 'password', 'alias')


class PostfixSerializer(serializers.ModelSerializer):
    emails = PostfixEmailSerializer(many=True)
    mysql_password = serializers.CharField(
        source='get_password', read_only=True)

    class Meta:
        model = models.Postfix


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ('id', 'server', 'type', 'name', 'domain')


class ProjectDetailSerializer(serializers.ModelSerializer):
    executables = serializers.ListField(
        source='get_executables', read_only=True)

    class Meta:
        model = models.Project
        depth = 4
        fields = '__all__'


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider


class ServerListSerializer(serializers.ModelSerializer):
    ips = serializers.StringRelatedField(many=True)
    main_ip = serializers.CharField(source='get_main_ip', read_only=True)

    class Meta:
        model = models.Server
        fields = (
            'id',
            'provider',
            'type',
            'code',
            'ips',
            'main_ip',
            'nginx_name',
            'control_dir'
        )


class ServerDetailSerializer(ServerListSerializer):
    ips = IpSerializer(many=True)

    class Meta(ServerListSerializer.Meta):
        depth = 1


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'server', 'db', 'type', 'name', 'is_active')


class UserDetailSerializer(UserListSerializer):
    password = serializers.CharField(source='get_password', read_only=True)

    class Meta(UserListSerializer.Meta):
        depth = 4
        fields = UserListSerializer.Meta.fields + ('password',)
