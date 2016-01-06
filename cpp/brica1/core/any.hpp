
#ifndef any_hpp_included_
#define any_hpp_included_

#ifdef __GNUG__
#	define USE_DEMANGLING (1)
#	include <cxxabi.h>
#endif

#include <iostream>
#include <typeinfo>
#include <stdexcept>
#include <cstring>
#include <memory>
#include <type_traits>

/***************************************************************************/

namespace type {
  struct any {
  private:
    struct i_type_holder {
      virtual ~i_type_holder() {}

      virtual bool is_empty() const = 0;
      virtual bool is_pointer() const = 0;
      virtual bool is_function_pointer() const = 0;
      virtual bool is_member_data_pointer() const = 0;
      virtual bool is_member_function_pointer() const = 0;
      virtual bool is_fundamental() const = 0;
      virtual bool is_compound() const = 0;
      virtual bool is_integral() const = 0;
      virtual bool is_signed() const = 0;
      virtual bool is_unsigned() const = 0;
      virtual bool is_floating() const = 0;
      virtual bool is_pod() const = 0;
      virtual bool is_array() const = 0;
      virtual bool is_enum() const = 0;
      virtual bool is_union() const = 0;
      virtual bool is_class() const = 0;
      virtual bool is_polymorphic() const = 0;

      virtual std::size_t size_of() const = 0;
      virtual std::size_t alignment_of() const = 0;

      virtual const std::type_info& type_id() const = 0;
      virtual const std::string type_name() const = 0;
    };

    template<typename T>
    struct type_holder: i_type_holder {
      T data_;

      type_holder(const T& v)
        :data_(v)
      {}
		
      bool is_empty() const
      { return std::is_empty<T>::value; }
      bool is_pointer() const
      { return std::is_pointer<T>::value; }
      bool is_function_pointer() const {
        return std::is_function<typename std::remove_pointer<T>::type>::value
          && std::is_pointer<T>::value;
      }
      bool is_member_data_pointer() const
      { return std::is_member_object_pointer<T>::value; }
      bool is_member_function_pointer() const
      { return std::is_member_function_pointer<T>::value; }
      bool is_fundamental() const
      { return std::is_fundamental<T>::value; }
      bool is_compound() const
      { return std::is_compound<T>::value; }
      bool is_integral() const
      { return std::is_integral<T>::value; }
      bool is_signed() const
      { return std::is_signed<T>::value; }
      bool is_unsigned() const
      { return std::is_unsigned<T>::value; }
      bool is_floating() const
      { return std::is_floating_point<T>::value; }
      bool is_pod() const
      { return std::is_pod<T>::value; }
      bool is_array() const
      { return std::is_array<T>::value; }
      bool is_enum() const
      { return std::is_enum<T>::value; }
      bool is_union() const
      { return std::is_union<T>::value; }
      bool is_class() const
      { return std::is_class<T>::value; }
      bool is_polymorphic() const
      { return std::is_polymorphic<T>::value; }

      std::size_t size_of() const
      { return sizeof(T); }
      std::size_t alignment_of() const
      { return std::alignment_of<T>::value; }

      const std::type_info& type_id() const
      { return typeid(T); }
      const std::string type_name() const
      { return demangle(type_id()); }

    private:
      std::string demangle(const std::type_info& ti) const {
#ifdef USE_DEMANGLING
        int stat;
        char* ptr = abi::__cxa_demangle(ti.name(), 0, 0, &stat);
        if ( !ptr ) return std::string();
        std::string str(ptr);
        ::free(ptr);
#else
        std::string str(ti.name());
#endif
        return str;
      }
    };

  public:
    template<typename T>
    any(const T& v)
      :data_(new type_holder<T>(v))
    {}
    any(const any &v)
      :data_(v.data_)
    {}
	
    bool is_empty() const
    { return data_->is_empty(); }
    bool is_pointer() const
    { return data_->is_pointer(); }
    bool is_function_pointer() const
    { return data_->is_function_pointer(); }
    bool is_member_data_pointer() const
    { return data_->is_member_data_pointer(); }
    bool is_member_function_pointer() const
    { return data_->is_member_function_pointer(); }
    bool is_fundamental() const
    { return data_->is_fundamental(); }
    bool is_compound() const
    { return data_->is_compound(); }
    bool is_integral() const
    { return data_->is_integral(); }
    bool is_signed() const
    { return data_->is_signed(); }
    bool is_unsigned() const
    { return data_->is_unsigned(); }
    bool is_floating() const
    { return data_->is_floating(); }
    bool is_pod() const
    { return data_->is_pod(); }
    bool is_array() const
    { return data_->is_array(); }
    bool is_enum() const
    { return data_->is_enum(); }
    bool is_union() const
    { return data_->is_union(); }
    bool is_class() const
    { return data_->is_class(); }
    bool is_polymorphic() const
    { return data_->is_polymorphic(); }

    std::size_t size_of() const
    { return data_->size_of(); }
    std::size_t alignment_of() const
    { return data_->alignment_of(); }

    const std::type_info& type_id() const
    { return data_->type_id(); }
    const std::string type_name() const
    { return data_->type_name(); }

    template<typename T>
    bool is_same() const
    { return (0 == strcmp(typeid(T).name(), data_->type_id().name())); }

    template<typename T>
    T& as() {
      if ( data_->is_pointer() ) {
        if ( !std::is_pointer<T>::value ) { throw std::bad_cast(); }
        return static_cast<type_holder<T>*>(data_.get())->data_;
      }
      if ( !is_same<T>() ) { throw std::bad_cast(); }
      return static_cast<type_holder<T>*>(data_.get())->data_;
    }
    template<typename T>
    const T& as() const {
      if ( data_->is_pointer() ) {
        if ( !std::is_pointer<T>::value ) { throw std::bad_cast(); }
        return static_cast<type_holder<T>*>(data_.get())->data_;
      }
      if ( !is_same<T>() ) { throw std::bad_cast(); }
      return static_cast<type_holder<T>*>(data_.get())->data_;
    }

    std::ostream& dump(std::ostream& os) const {
      return os
        << std::boolalpha
#if __cplusplus == 201103L
        << "type_id                   : " << type_id().hash_code() << std::endl
#endif
        << "type_name                 : " << type_name() << std::endl
        << "size_of                   : " << size_of() << std::endl
        << "alignment_of              : " << alignment_of() << std::endl
        << "is_empty                  : " << is_empty() << std::endl
        << "is_pointer                : " << is_pointer() << std::endl
        << "is_function_pointer       : " << is_function_pointer() << std::endl
        << "is_member_data_pointer    : " << is_member_data_pointer() << std::endl
        << "is_member_function_pointer: " << is_member_function_pointer() << std::endl
        << "is_fundamental            : " << is_fundamental() << std::endl
        << "is_compound               : " << is_compound() << std::endl
        << "is_integral               : " << is_integral() << std::endl
        << "is_signed                 : " << is_signed() << std::endl
        << "is_unsigned               : " << is_unsigned() << std::endl
        << "is_floating               : " << is_floating() << std::endl
        << "is_pod                    : " << is_pod() << std::endl
        << "is_array                  : " << is_array() << std::endl
        << "is_enum                   : " << is_enum() << std::endl
        << "is_union                  : " << is_union() << std::endl
        << "is_class                  : " << is_class() << std::endl
        << "is_polymorphic            : " << is_polymorphic() << std::endl
        ;
    }

  private:
    std::shared_ptr<i_type_holder> data_;
  };

  /***************************************************************************/
}

#endif // any_hpp_included_
