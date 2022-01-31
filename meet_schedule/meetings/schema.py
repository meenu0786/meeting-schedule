from datetime import timedelta
import graphene
from graphene_django import DjangoObjectType
from .models import Schedule, NonUser
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from django.db.models import Q

# Signup & Signin ----------->>

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()


class ScheduleType(DjangoObjectType):
    class Meta:
        model = Schedule
        fields = '__all__'


class NonUserType(DjangoObjectType):
    class Meta:
        model = NonUser
        fields = '__all__'

# Show all meetings list ------->>


class Query(UserQuery, MeQuery, graphene.ObjectType):
    all_users = graphene.List(ScheduleType)

    def resolve_all_users(self, *args, **kwargs):
        return Schedule.objects.all()


# Inputs Meeting Details ------->>

class MeetInput(graphene.InputObjectType):
    user = graphene.Int()
    start_date_time = graphene.DateTime()
    interval_time = graphene.String()


# # Create new Meet ---------->>

def check_overlapping_schedule(start_date_time, interval_time):
    end_date_time = start_date_time + timedelta(minutes=int(interval_time))

    overlapping_slots = Schedule.objects.filter(Q(start_date_time__lte=start_date_time, end_date_time__gte=start_date_time) | Q(start_date_time__lte=end_date_time, end_date_time__gte=end_date_time))

    return overlapping_slots, end_date_time


class CreateMeet(graphene.Mutation):
    class Arguments:
        input = MeetInput(required=True)
    data = graphene.Field(ScheduleType)

    @classmethod
    def mutate(cls, root, info, input):
        if info.context.user and info.context.user.is_authenticated:
            schedule = Schedule()
            schedule.user_id = info.context.user.id
            schedule.start_date_time = input.start_date_time
            schedule.interval_time = input.interval_time

            overlapping_slots, end_date_time = check_overlapping_schedule(input.start_date_time, input.interval_time)
            # end_date_time = input.start_date_time + \
            #     timedelta(minutes=int(input.interval_time))

            schedule.end_date_time = end_date_time
            
            # overlapping_slots = Schedule.objects.filter(Q(start_date_time__lte=input.    start_date_time, end_date_time__gte=input.start_date_time) | Q(start_date_time__lte=end_date_time, end_date_time__gte=end_date_time))

            if not overlapping_slots.exists():
                schedule.save()
                return CreateMeet(data=schedule)
            else:
                raise Exception("Schedule alredy exists!")
        else:
            raise Exception("Authentication credentials were not provided")


# # Update Meet ---------->>

class UpdateMeet(graphene.Mutation):
    class Arguments:
        input = MeetInput(required=True)
        id = graphene.ID()

    data = graphene.Field(ScheduleType)

    @classmethod
    def mutate(cls, root, info, input, id):
        if info.context.user and info.context.user.is_authenticated:
            schedule = Schedule.objects.get(pk=id)
            schedule.user_id = info.context.user.id

            start_date_time = input.start_date_time if input.start_date_time else schedule.start_date_time
            interval_time = input.interval_time if input.interval_time else schedule.interval_time
            overlapping_slots, end_date_time = check_overlapping_schedule(start_date_time,interval_time)

            schedule.end_date_time = end_date_time
            schedule.start_date_time = start_date_time
            schedule.interval_time = interval_time

            if not overlapping_slots.exists():
                schedule.save()
                return UpdateMeet(data=schedule)
            else:
                raise Exception("Schedule alredy exists!")
        else:
            raise Exception("Authentication credentials were not provided")


# # Delete Meet ---------->>

class DeleteMeet(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        if info.context.user and info.context.user.is_authenticated:
            schedule = Schedule.objects.get(pk=kwargs["id"])
            schedule.delete()
            return cls(ok=True)
        else:
            raise Exception("Authentication credentials were not provided")


# # Show all Meet List ---------->>

class ScheduleList(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    data = graphene.List(ScheduleType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        if kwargs["id"]:
            schedule_list = Schedule.objects.filter(user_id=kwargs["id"])
            return ScheduleList(data=schedule_list)

# # ----------------------------------------------------------------------------
# # Non-User Reserve Meetings
# # ------------------------------------------------------------------------------

# Non-User Inputs Details ------->>


class NonUserInput(graphene.InputObjectType):
    schedule = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()

# Reserve new Meet ---------->>


class CreateReserve(graphene.Mutation):

    class Arguments:
        input = NonUserInput(required=True)
    data = graphene.Field(NonUserType)

    @classmethod
    def mutate(cls, root, info, input):
        if not NonUser.objects.filter(schedule_id=input.schedule).exists():
            Non_User = NonUser()
            Non_User.schedule_id = input.schedule
            Non_User.first_name = input.first_name
            Non_User.last_name = input.last_name
            Non_User.email = input.email
            Non_User.save()
            return CreateReserve(data=Non_User)
        else:
            raise Exception("Already Reserved!!")


# CRUD Perform--------------->>

class Mutation(AuthMutation, graphene.ObjectType):
    create_meet = CreateMeet.Field()
    create_reserve = CreateReserve.Field()
    update_meet = UpdateMeet.Field()
    schedule_list = ScheduleList.Field()
    delete_meet = DeleteMeet.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
